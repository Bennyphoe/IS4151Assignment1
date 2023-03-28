import serial
import time
import sqlite3
import bme280
from datetime import datetime
import subscriber

fogName = "fogProcessor1"
fireTemperature = 30
fireLightLevel = 0.8
localFireAlarm = False
bme280.toggleLed(False)
predefinedNodes = ['vapaz', 'togez']

def sendCommand(command):
		
	command = command + '\n'
	ser.write(str.encode(command))

def reconnect():
	reconnect = "rs="
	concatNodes = ",".join(predefinedNodes)
	# Handshaking
	sendCommand(reconnect + concatNodes)

def receivedMessageFromBroker(payload):
    print(payload)

def doHandShake():
	strMicrobitDevices = ''
	handShake = "hs="
	concatNodes = ",".join(predefinedNodes)
	# Handshaking
	sendCommand(handShake + concatNodes)

	while strMicrobitDevices == None or len(strMicrobitDevices) <= 0:
		strMicrobitDevices = waitResponse()
		time.sleep(0.1)
	strMicrobitDevices = strMicrobitDevices.split('=')
	print(strMicrobitDevices)
	
	if len(strMicrobitDevices[1]) > 0:
		listMicrobitDevices = strMicrobitDevices[1].split(',')
		if len(listMicrobitDevices) > 0:
			for mb in listMicrobitDevices:
				print('Connected to micro:bit device {}...'.format(mb))
    

def sendCommandToNodes():
	global predefinedNodes
	while True:
		print('Sending command to all micro:bit devices...')
		commandToTx = 'sensor=readings'				
		sendCommand('cmd:' + commandToTx)
		print('Finished sending command to all micro:bit devices...')
		
		if commandToTx.startswith('sensor='):
			
			strSensorValues = ''

			while strSensorValues == None or len(strSensorValues) <= 0:
				
				strSensorValues = waitResponse()
				time.sleep(0.1)
		sensorValues = strSensorValues.split(',')
		if (len(sensorValues) == len(predefinedNodes)):
			return strSensorValues.split(',')
		else:
			reconnect()
			time.sleep(3) # allow enough time to reconnect
			print("Didnt receive all nodes values, trying again")
			
		

def waitResponse():
	
	response = ser.readline()
	response = response.decode('utf-8').strip()
	return response

def checkForFire(readings):
	for reading in readings:
		data = reading.split('=')
		dataReadings = data[1].split("-")
		temp = int(dataReadings[0])
		lightLevel = dataReadings[1]
		if ("fogProcessor" not in data[0]):
			intLightLevel = int(lightLevel)
			roundedLightLevel = round((intLightLevel / 255), 3)
			if (temp > fireTemperature and roundedLightLevel > fireLightLevel):
				return data[0]
		else:
			if (temp > fireTemperature and float(lightLevel) > fireLightLevel):
				return data[0]
	return False

def saveData(readings):
	c = conn.cursor()
	
	for reading in readings:
		data = reading.split('=')
		dataReadings = data[1].split("-")
		temp = dataReadings[0]
		lightLevel = dataReadings[1]
		if ("fogProcessor" not in data[0]):
			intLightLevel = int(lightLevel)
			roundedLightLevel = round((intLightLevel / 255), 3)
			stringLightLevel = str(roundedLightLevel)         
			sql = "INSERT INTO readings (devicename, temp, lightlevel, timestamp) VALUES('" + data[0] + "', " + temp + ", " + stringLightLevel + ", datetime('now', 'localtime'))"
			
		else:
			
			sql = "INSERT INTO readings (devicename, temp, lightlevel, timestamp) VALUES('{}','{}','{}',datetime('now', 'localtime'))".format(data[0], temp, lightLevel)
		c.execute(sql)
	conn.commit()
	
	readings.clear()
		
def saveOutbreak(source):
	c = conn.cursor()
	sql = "INSERT INTO outbreaks (source, timestamp) VALUES ('{}',datetime('now', 'localtime'))".format(source)
	c.execute(sql)
	conn.commit()
	
def triggerAlarm(toggle):
	bme280.toggleLed(toggle)
# 	need to send radio signal to rcontroller
	sendCommand("localFire")
	print("local fire alarm activated!")


try:

	print("Listening on /dev/ttyACM0... Press CTRL+C to exit")	
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
	conn = sqlite3.connect('readings.db')	
	subscriber.run(receivedMessageFromBroker)
	doHandShake()
	while True:
		time.sleep(5)
		listSensorValues = []
		if not localFireAlarm:
			if (len(predefinedNodes) > 0):
				listSensorValues = sendCommandToNodes()
					
			# together with sensor values we also have to persist data coming from rpi
			fogReadings = bme280.getTemperatureAndLightLevel()
			listSensorValues.append("{}={}-{}".format(fogName, fogReadings["temp"], fogReadings["lightLevel"]))

			for sensorValue in listSensorValues:
				print(sensorValue)

			source = checkForFire(listSensorValues)
			if source:
				saveOutbreak(source)
				localFireAlarm = True
				triggerAlarm(True)
						
			else:
				saveData(listSensorValues)
		else:
			reconnect()
			time.sleep(0.2)
			triggerAlarm(True)
			print("pending deactivation")

except KeyboardInterrupt:
		
	print("Program terminated!")

except:

	print('********** UNKNOWN ERROR')

finally:
	
	if ser.is_open:
		ser.close()
		
	conn.close()


