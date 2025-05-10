import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from org_reader import OrgReader

if   __name__  ==  "__main__":
    testorg = Path.cwd() / "org-roam.db"
    reader = OrgReader()
    print(reader.load_data())
