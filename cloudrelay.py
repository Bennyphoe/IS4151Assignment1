import time
import sqlite3
import requests
import json

try:
    conn = sqlite3.connect("readings.db")
    base_uri = "http://192.168.1.61:5000/"
    globalreading_uri = base_uri + "api/readings"
    headers = {'content-type': 'application/json'}
    
    while True:
        time.sleep(10)
        
        print("relaying data to cloud")
        
        c = conn.cursor()
        c.execute("SELECT * from readings WHERE tocloud = 0")
        results = c.fetchall()
        c = conn.cursor()
        
        for result in results:
            print("Relaying id={}; devicename={}; temp={}; lightlevel={}; timestamp={}".format(result[0], result[1], result[2], result[3], result[4]))
            reading = {
                'devicename': result[1],
                'temp': result[2],
                'lightlevel': result[3],
                'timestamp': result[4]
            }
            req = requests.put(globalreading_uri, headers = headers, data = json.dumps(reading))
            c.execute('UPDATE readings SET tocloud = 1 WHERE id = "{}"'.format(result[0]))
        conn.commit()
        
except KeyboardInterrupt:
    print("END")
except Error as err:
    print("error: {}".format(err))
finally:
    conn.close()
            