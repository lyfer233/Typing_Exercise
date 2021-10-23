import sqlite3
from constants import WindowConstants as wc

a = ()
conn = sqlite3.connect(wc.WORDLIST_PATH)
cur = conn.cursor()
cur.execute("SELECT * FROM word WHERE is_delete=0 LIMIT 30")
a = tuple(cur.fetchall())
print(a)