import sqlite3
import json
from shapely.geometry import asShape


db = sqlite3.connect('../../data/permits/urban-dev.sqlite')
cur = db.cursor()

sql = "SELECT id, name, geometry, area FROM neighborhoods"
for row in cur.execute(sql):
   shape = asShape(json.loads(row[2]))
   print("INSERT INTO neighborhoods2 (shape, name, area) VALUES(" + "GeomFromText('" + shape.wkt + "'), " + "'" + row[1].replace("'", "''") + "', " + str(row[3]) + ");")


