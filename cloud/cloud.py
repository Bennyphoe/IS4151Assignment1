import mysql.connector
from flask import Flask, render_template, request
import publisher
from flask_cors import CORS
import json
import readings
import outbreaks as outbreakModule
import threading

app = Flask(__name__, template_folder='../templates', static_folder="../static")
CORS(app)


# Cloud UI
@app.route('/', methods=['GET'])
def index():
    sensorReadings = readings.read()
    outbreaks = outbreakModule.read()
    
    return render_template('cloud.html', readings = sensorReadings, outbreaks = outbreaks)


# POST request to save sensor data into cloud
@app.route("/readings", methods=["POST"])
def postSensorData():
    payload = request.get_json()
    return readings.create(payload)

# POST request to save outbreaks into cloud
@app.route("/outbreaks", methods=["POST"])
def postOutbreak():
    payload = request.get_json()
    return outbreakModule.create(payload)
    
@app.route("/outbreaks", methods=["PUT"])
def updateOutbreak():
    payload = request.get_json()
    response = outbreakModule.update(payload["status"], payload["id"])
    source = payload["deviceName"]
    if payload["status"] == "triggered":
        publisher.publishMessage("trigger", source)
    elif payload["status"] == "resolved":
        publisher.publishMessage("resolve", source)
    return response
    
    

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False,  use_reloader=False)).start()
    publisher.run()
    
