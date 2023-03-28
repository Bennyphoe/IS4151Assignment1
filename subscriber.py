import random
import paho.mqtt.client as mqtt
import threading



def on_connect(client, userdata, flags, rc):
	
	if rc == 0:
	
		print("Connected to MQTT Broker!")
		
	else:
	
		print('Failed to connect, return code {:d}'.format(rc))



def on_message(client, userdata, msg, callback):
	
	print('Received {} from {} topic'.format(msg.payload.decode(), msg.topic))
	callback(msg.payload.decode())

def mqttSubscriber(callback):
	broker = 'broker.emqx.io'
	port = 1883
	topic = "/firealarm/ia1"
	client_id = f'python-mqtt-{random.randint(0, 10000)}'
	username = 'emqx'
	password = 'public'

	print('client_id={}'.format(client_id))



	# Set Connecting Client ID
	client = mqtt.Client(client_id)
	client.username_pw_set(username, password)
	client.on_connect = on_connect
	client.connect(broker, port)
	
	client.subscribe(topic)
	client.on_message = on_message(callback)

	client.loop_forever()	
 
def run(callback):
	mqtt_thread = threading.Thread(target=mqttSubscriber, args =(callback,))
	mqtt_thread.start()

