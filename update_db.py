import sqlite3
from device import Device
import time

conn = sqlite3.connect('db.sqlite3')
sql_query = "SELECT * FROM dashboard_device;"
cursor = conn.cursor()
cursor.execute(sql_query)
data = cursor.fetchall()
devices= []
for d in data:
    
    devices.append(Device(d[1],d[2],d[3],d[4],d[5]))

while True:
    for device in devices:
        done = device.initialize()
        if done:
            device.update()
            time.sleep(1)
    
    
