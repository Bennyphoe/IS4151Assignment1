import time
import sqlite3
import requests
import json

base_uri = "http://192.168.1.61:5000/"
globalreading_uri = base_uri + "/readings"
globaloutbreak_uri = base_uri + "/outbreaks"
headers = {'content-type': 'application/json'}

def relayEventsToCloud(conn):
    c = conn.cursor()
    c.execute("SELECT * from outbreaks WHERE tocloud = 0")
    results = c.fetchall()
    for result in results:
        print("Relaying id={}; source={}; timestamp={}".format(result[0], result[1], result[2]))
        outbreak = {
            'source': result[1],
            'timestamp': result[2]
        }
        req = requests.post(globaloutbreak_uri, headers = headers, data = json.dumps(outbreak))
        c.execute('UPDATE outbreaks SET tocloud = 1 WHERE id = "{}"'.format(result[0]))
    conn.commit()

def relayReadingsToCloud(conn):
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
        req = requests.post(globalreading_uri, headers = headers, data = json.dumps(reading))
        c.execute('UPDATE readings SET tocloud = 1 WHERE id = "{}"'.format(result[0]))
    conn.commit()   

try:
    conn = sqlite3.connect("readings.db")
    
    while True:
        time.sleep(10)
        print("relaying readings to cloud")
        relayReadingsToCloud(conn)
        print("relaying outbreaks to cloud")
        relayEventsToCloud(conn)
        print("all relayed!")
        
        
        
except KeyboardInterrupt:
    print("END")
except Exception as err:
    print("error: {}".format(err))
finally:
    conn.close()
            