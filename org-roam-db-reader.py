from pathlib import Path
import orgparse
import sqlite3
import argparse


class OrgRoamDbReader:
    def  __init__(self):
        self.db_file = Path.cwd() / "org-roam.db"
        self.roam_path = Path.cwd() / "org-roam"
        self._parse_args()
        self._init_database()
        self._read_nodes()
        self._read_tags()
        self._read_links()

    def _read_nodes(self):
        rows = self.query_table("nodes")
        self.nodes = {}
        for row in rows:
            node = {
                "id":row[0].strip('"'),
                "file":row[1].strip('"'),
                "title":row[8].strip('"'),
                "tags":[],
                "links_to":[]
             }
            self.nodes[node["id"]] = node

    def _read_tags(self):
        rows = self.query_table("tags")
        for row in rows:
            id = row[0].strip('"')
            node = self.nodes[id]
            node["tags"].append(row[1].strip('"'))

    def _read_links(self):
        rows = self.query_table("links")
        for row in rows:
            source_id = row[1].strip('"')
            dest_id = row[2].strip('"')
            node = self.nodes[source_id]
            if dest_id in self.nodes:
                dest_node = self.nodes[dest_id]
                node["links_to"].append(dest_node["title"])

    def   _init_database(self):
        self.conn = sqlite3.connect(self.db_file)

    def   _parse_args(self):
        parser = argparse.ArgumentParser(description="Org-roam database reader.")
        parser.add_argument("--db", help="Path to the org-roam database file.", default=None)
        parser.add_argument("--dir", help="Path to the directory containing Org Roam files")
        args = parser.parse_args()

        if args.db:
            self.db_file = Path(args.db)
        if args.dir:
            self.roam_path = args.dir

    def query_table(self,table:str):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+table)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_context(self,id):
        file = self.nodes[id]["file"]
        root = orgparse.load(file)
        for node in root:
            print(node)
        return root

if   __name__  ==  "__main__":
    reader = OrgRoamDbReader()
    id = 'e7e2456e-e18d-44e9-93a4-9a990f77e0e6'
    print(reader.get_context(id))
