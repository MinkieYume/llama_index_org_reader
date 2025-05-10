import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pathlib import Path
from org_roam_db_reader import OrgRoamDbReader

if   __name__  ==  "__main__":
    db_file = Path.cwd() / "org-roam.db"
    reader = OrgRoamDbReader()
    print(reader.load_data(db_file))
