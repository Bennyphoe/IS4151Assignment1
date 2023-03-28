import random
import time
import mysql.connector
from trigger import Trigger
import paho.mqtt.client as mqtt

topic = "/firealarm/ia1"

def on_connect(client, userdata, flags, rc):
	
	if rc == 0:
	
		print("Connected to MQTT Broker!")
		
	else:
	
		print('Failed to connect, return code {:d}'.format(rc))

def retrievePendingOutbreak(conn):
	c = conn.cursor()
	c.execute('SELECT * FROM outbreaks WHERE status = "{}"'.format(Trigger.PENDING.value))
	results = c.fetchall()
	if len(results) > 0:
		event = results[0]
		return event
	else:
		return False
	
 

def retrieveTriggeredOutbreak(conn):
	c = conn.cursor()
	c.execute('SELECT * FROM outbreaks WHERE status = "{}"'.format(Trigger.TRIGGERED.value))
	results = c.fetchall()
	if len(results) > 0:
		event = results[0]
		return event
	else:
		return False

def updateOutbreakStatus(conn, status, id):
	print(id)
	c = conn.cursor()
	sql = 'UPDATE outbreaks SET status = "{}" WHERE id = {}'.format(status, id)
	c.execute(sql)
	conn.commit()
	print("Updated status successfully")

def getStatus(result, msg):
	global topic
	# result: [0, 1]
	status = result[0]
	
	if status == 0:
		print('Send {} to topic {}'.format(msg, topic))
	else:
		print('Failed to send message to topic {}'.format(topic))

def run():
	try:
		broker = 'broker.emqx.io'
		port = 1883
		client_id = f'python-mqtt-{random.randint(0, 10000)}'
		username = 'emqx'
		password = 'public'

		print('client_id={}'.format(client_id))

		conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='readings',
		autocommit = True
	)

		# Set Connecting Client ID
		client = mqtt.Client(client_id)
		client.username_pw_set(username, password)
		client.on_connect = on_connect
		client.connect(broker, port)

		client.loop_start()
		
		while True:
			time.sleep(5)
			result = ''
			pendingOutbreak = retrievePendingOutbreak(conn)
			if pendingOutbreak:
				userInput = input("enter `trigger` to trigger global alarm or `resolve` to resolve local alarm")
				if (userInput== "trigger"):
					msg = "global:" + pendingOutbreak[1]
					result = client.publish(topic, msg)
					updateOutbreakStatus(conn, Trigger.TRIGGERED.value, pendingOutbreak[0])
					
				elif userInput == "resolve":
					msg = "resolve"
					result = client.publish(topic, msg)
					updateOutbreakStatus(conn, Trigger.RESOLVED.value, pendingOutbreak[0])
				else:
					continue
			else:
				triggeredOutbreak = retrieveTriggeredOutbreak(conn)
				if (triggeredOutbreak):
					userInput = input("enter `resolve` to resolve local/global alarm")
					if (userInput == "resolve"):
						msg = "resolve"
						result = client.publish(topic, msg)
						updateOutbreakStatus(conn, Trigger.RESOLVED.value, triggeredOutbreak[0])
					else:
						continue
			if result and msg:
				getStatus(result, msg)

	except KeyboardInterrupt:

			print('Program terminated!')



if __name__ == '__main__':
	
	run()