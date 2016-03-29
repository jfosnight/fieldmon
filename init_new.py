import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS node \
    (id INTEGER PRIMARY KEY ASC, \
    name TEXT DEFAULT NULL, \
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP)")

c.execute("CREATE TABLE IF NOT EXISTS image \
    (id INTEGER PRIMARY KEY ASC, \
    file_name, \
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP)")
conn.commit()
conn.close()
