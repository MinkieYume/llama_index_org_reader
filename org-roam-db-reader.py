#!/usr/bin/env python3
import sqlite3
from pathlib import Path

def get_db_path(root):
    return Path(root).joinpath("org-roam").joinpath("org-roam.db")

def get_title_and_content(db_path, node_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT title, content FROM nodes WHERE id = ?""", (node_id,))
    result = cursor.fetchone()
    conn.close()

    return result
