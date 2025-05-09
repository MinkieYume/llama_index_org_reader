#!/usr/bin/env python3
from pathlib import Path
import sqlite3
import argparse

class OrgRoamDbReader:
    def    __init__(self):
        self.db_file = Path.home()     /   "org-roam/org-roam.db"
        self.roam_path = Path.home()     /   "org-roam"

    def _read_nodes():
        pass

    def parse_args():
        parser = argparse.ArgumentParser(description="Org Roam Database Reader")
        parser.add_argument("--db", help="Path to the Org Roam database file")
        parser.add_argument("--dir", help="Path to the directory containing Org Roam files")
        args = parser.parse_args()
        if args.db:
            self.db_file = args.db
        if args.dir:
            self.roam_path = args.dir

if  __name__      ==   "__main__":
    args = OrgRoamDbReader.parse_args()
    reader = OrgRoamDbReader()
