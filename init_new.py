import sqlite3
import os

print("Setting Up Database")
conn = sqlite3.connect("data.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS node \
    (id INTEGER PRIMARY KEY ASC, \
    name TEXT DEFAULT NULL, \
    lat TEXT, \
    lng TEXT, \
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP)")

c.execute("CREATE TABLE IF NOT EXISTS image \
    (id INTEGER PRIMARY KEY ASC, \
    file_name TEXT, \
    lat TEXT, \
    lng TEXT, \
    alt TEXT, \
    heading TEXT, \
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP)")

## Setup Sensor Data Table
c.execute("CREATE TABLE IF NOT EXISTS sensor_data \
    (\
    id INTEGER PRIMARY KEY ASC, \
    node_id INT, \
    temperature REAL, \
    humidity REAL, \
    soil_moisture REAL, \
    pressure REAL, \
    timestamp TEXT \
    )\
")
conn.commit()
conn.close()
print("Database Setup")


print("Creating Directories")
if not os.path.isdir("./images"):
    os.makedirs("./images")


print("Setting up Bower")
from subprocess import call
call(["bower", "install", "--allow-root"])
