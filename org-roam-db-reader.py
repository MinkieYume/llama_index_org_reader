from pathlib import Path
import sqlite3
import argparse


class OrgRoamDbReader:
    def __init__(self):
        self.db_file = Path.cwd() / "org-roam.db"
        self.roam_path = Path.cwd() / "org-roam"
        self._parse_args()
        self._init_database()

    def read_nodes(self):
        var rows = self.query_table("nodes")
        for row in rows:
            pass

    def query_table(self,table : str):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+table)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    
    def _init_database(self):
        self.conn = sqlite3.connect(self.db_file)

    def _parse_args(self):
        parser = argparse.ArgumentParser(description="Org-roam database reader.")
        parser.add_argument("--db", help="Path to the org-roam database file.", default=None)
        parser.add_argument("--dir", help="Path to the directory containing Org Roam files")
        args = parser.parse_args()

        if args.db:
            self.db_file = Path(args.db)
        if args.dir:
            self.roam_path = args.dir

if __name__ == "__main__":
    reader = OrgRoamDbReader()
    reader.read_nodes()
