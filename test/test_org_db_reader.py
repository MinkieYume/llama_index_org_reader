import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pathlib import Path
from org_roam_db_reader import OrgRoamDbReader

if   __name__  ==  "__main__":
    db_file = Path.cwd() / "org-roam.db"
    reader = OrgRoamDbReader(db_file)
    id = 'e7e2456e-e18d-44e9-93a4-9a990f77e0e6'
    print(reader.get_context(id))
