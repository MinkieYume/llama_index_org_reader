import argparse


class OrgRoamDbReader:
    def     __init__(self):
        self.db_file = Path.home() / "org-roam/org-roam.db"

    def    _read_nodes(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT nodes FROM org_node")
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Org-roam database reader.")
        parser.add_argument("--db", help="Path to the org-roam database file.", default=None)
        args = parser.parse_args()

        if args.db:
            self.db_file = Path(args.db)

if     __name__    ==    "__main__":
    reader = OrgRoamDbReader()
    reader.parse_args()
    print(reader._read_nodes())
