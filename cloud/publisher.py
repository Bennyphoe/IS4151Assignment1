import random
import time
import mysql.connector
from trigger import Trigger
import paho.mqtt.client as mqtt
import threading

topic = "/firealarm/ia1"

def on_connect(client, userdata, flags, rc):
	
	if rc == 0:
		print("Connected to MQTT Broker!")
	else:
		print('Failed to connect, return code {:d}'.format(rc))

def getStatus(result, msg):
	global topic
	# result: [0, 1]
	status = result[0]
	
	if status == 0:
		print('Send {} to topic {}'.format(msg, topic))
	else:
		print('Failed to send message to topic {}'.format(topic))

def mqttPublisher():
	global client
	try:
		broker = 'broker.emqx.io'
		port = 1883
		client_id = f'python-mqtt-{random.randint(0, 10000)}'
		username = 'emqx'
		password = 'public'

		print('client_id={}'.format(client_id))

		# Set Connecting Client ID
		client = mqtt.Client(client_id)
		client.username_pw_set(username, password)
		client.on_connect = on_connect
		client.connect(broker, port)

		client.loop_start()
	except Exception as error:
		print(error)
  
  
def publishMessage(userInput, deviceName):
	print(userInput + deviceName)
	if (userInput == "trigger"):
		msg = "global:" + deviceName
		result = client.publish(topic, msg)
			
	elif userInput == "resolve":
		msg = "resolve"
		result = client.publish(topic, msg)
	

def run():
	mqtt_thread = threading.Thread(target=mqttPublisher)
	mqtt_thread.start()