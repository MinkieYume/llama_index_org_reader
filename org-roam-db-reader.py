#!/usr/bin/env python3
import sqlite3
from pathlib import Path

class OrgRoamDbReader:
    def __init__(self, db_file,roam_path):
        self.db_file = db_file
        self.roam_path = roam_path

    def get_db_path(self):
        return Path(self.root).joinpath("org-roam").joinpath("org-roam.db")

    def get_title_and_content(self, node_id):
        db_path = self.get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""SELECT title, content FROM nodes WHERE id = ?""", (node_id,))
        result = cursor.fetchone()
        conn.close()

        return result

if __name__ == "__main__":
    reader = OrgRoamDbReader()
