import sqlite3
import os

print("Setting Up Database")
conn = sqlite3.connect("data.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS node \
    (id INTEGER PRIMARY KEY ASC, \
    name TEXT DEFAULT NULL, \
    lat, \
    lng, \
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP)")

c.execute("CREATE TABLE IF NOT EXISTS image \
    (id INTEGER PRIMARY KEY ASC, \
    file_name, \
    lat, \
    lng, \
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP)")
conn.commit()
conn.close()
print("Database Setup")


print("Creating Directories")
if not os.path.isdir("./images"):
    os.makedirs("./images")


print("Setting up Bower")
from subprocess import call
call(["bower", "install", "--allow-root"])
