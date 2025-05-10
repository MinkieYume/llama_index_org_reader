import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from org_reader import OrgReader
from pathlib import Path

if   __name__  ==  "__main__":
    file = Path.cwd() / "test_file.org"
    reader = OrgReader()
    print(reader.load_data(file))
