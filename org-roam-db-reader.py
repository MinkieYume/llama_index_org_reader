#!/usr/bin/env python3
import sqlite3
from pathlib import Path
import sys

class OrgRoamDbReader:
    def __init__(self, db_file, roam_path):
        self.db_file   = db_file
        self.roam_path   = roam_path

    def read(self):
        conn   = sqlite3.connect(self.db_file)
        cur    = conn.cursor()
        cur.execute("SELECT * FROM nodes")
        rows   = cur.fetchall()
        for row in rows:
            print(row)

if __name__  == "__main__":
    db_file     = Path.home()  / "org-roam/org-roam.db"
    roam_path   = Path.home()  / "org-roam"
    reader      = OrgRoamDbReader(db_file, roam_path)
    reader.read()
