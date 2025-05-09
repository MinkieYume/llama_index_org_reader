#!/usr/bin/env python3
import sqlite3
from pathlib import Path

class OrgRoamDbReader:
    def __init__(self, db_file, roam_path):
        self.db_file = db_file
        self.roam_path = roam_path

if __name__ == "__main__":
    reader = OrgRoamDbReader()
