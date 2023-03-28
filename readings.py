import mysql.connector
from flask import make_response, abort



def read():
	
	readings = []
	
	conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='readings'
	)
	
	c = conn.cursor()
	c.execute('SELECT devicename, AVG(temp) AS averagetemp, AVG(lightlevel) AS averageLightLevel FROM readings GROUP BY devicename ORDER BY devicename ASC')
	results = c.fetchall()
	
	for result in results:
				
		readings.append({'devicename':result[0],'averagetemp':result[1], 'averagelightlevel': result[2]})
	
	conn.close()
	
	return readings



def create(globalReading):
	print(globalReading)
	'''
	This function creates a new reading record in the database
	based on the passed in reading data
	:param globalreading:  Global reading record to create in the database
	:return:        200 on success
	'''
	devicename = globalReading.get('devicename', None)
	temp = globalReading.get('temp', None)
	lightlevel = globalReading.get('lightlevel', None)
	timestamp = globalReading.get('timestamp', None)

	conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='readings'
	)

	c = conn.cursor()	
	sql = "INSERT INTO readings (devicename, temp, lightlevel, timestamp) VALUES('{}', {}, {}, '{}')".format(devicename, temp, lightlevel, timestamp)
	print(sql)
	c.execute(sql)
	conn.commit()
	conn.close()

	return make_response('Global reading record successfully created', 200)
