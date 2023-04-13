import mysql.connector
from flask import make_response, abort

try:
	conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='readings',
  		autocommit = True
	)

except Exception as error:
    print(error)

def read():
	
	readings = []
	c = conn.cursor()
	c.execute('SELECT devicename, temp, lightlevel FROM readings ORDER BY devicename ASC')
	results = c.fetchall()
	for result in results:
		readings.append({'devicename':result[0],'temperature':result[1], 'lightlevel': result[2]})
	print(readings)
	return readings



def create(body):
	print(body)
	'''
	This function creates a new reading record in the database
	based on the passed in reading data
	:param globalreading:  Global reading record to create in the database
	:return:        200 on success
	'''
	devicename = body["devicename"]
	temp = body["temp"]
	lightlevel = body["lightlevel"]
	timestamp = body["timestamp"]

	c = conn.cursor()	
	sql = "INSERT INTO readings (devicename, temp, lightlevel, timestamp) VALUES('{}', {}, {}, '{}')".format(devicename, temp, lightlevel, timestamp)
	print(sql)
	c.execute(sql)
	conn.commit()

	return make_response('Global reading record successfully created', 200)
