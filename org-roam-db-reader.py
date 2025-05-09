from pathlib import Path
import sqlite3
import argparse


class OrgRoamDbReader:
    def __init__(self):
        self.db_file = Path.cwd() / "org-roam.db"
        self.roam_path = Path.cwd() / "org-roam"
        print(self.db_file)

    def _read_nodes(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM nodes")
        rows = cursor.fetchall()
        cursor.close()
        return [row[0] for row in rows]

    def init_database():
        conn = sqlite3.connect(self.db_file)

    def parse_args(self):
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
    reader.parse_args()
    print(reader._read_nodes())
