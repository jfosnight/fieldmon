import sqlite3
import os

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


if not os.path.isdir("./images"):
    os.makedirs("./images")


from subprocess import call
call(["bower", "install"])
