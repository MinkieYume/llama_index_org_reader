#!/usr/bin/env python3
import sqlite3
from pathlib import Path
import argparse

class OrgRoamDbReader:
    def  __init__(self, db_file, roam_path):
        self.db_file    = db_file
        self.roam_path    = roam_path

    def read(self):
        conn     = sqlite3.connect(self.db_file)
        cur      = conn.cursor()
        cur.execute("SELECT * FROM nodes")
        rows     = cur.fetchall()
        for row in rows:
            print(row)

if __name__    == "__main__":
    db_file       = Path.home()   / "org-roam/org-roam.db"
    roam_path     = Path.home()   / "org-roam"

    parser        = argparse.ArgumentParser(description="Org Roam Database Reader")
    parser.add_argument("--db", help="Path to the Org Roam database file")
    parser.add_argument("--dir", help="Path to the directory containing Org Roam files")
    args          = parser.parse_args()

    if args.db:
        db_file   = args.db
    if args.dir:
        roam_path   = args.dir

    reader        = OrgRoamDbReader(db_file, roam_path)
    reader.read()
