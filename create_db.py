"""Create db"""

import sqlite3

from views import site

con = sqlite3.connect('patterns.sqlite')
cur = con.cursor()
with open('create_db.sql', 'r', encoding="utf-8") as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()
