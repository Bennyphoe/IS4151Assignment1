import mysql.connector
from flask import make_response, abort



def read():
	
	outbreaks = []
	
	conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='readings'
	)
	
	c = conn.cursor()
	c.execute('SELECT source, timestamp FROM outbreaks ORDER BY source ASC')
	results = c.fetchall()
	
	for result in results:
				
		outbreaks.append({'source':result[0],'timestamp':result[1]})
	
	conn.close()
	
	return outbreaks



def create(globalOutbreak):
	print(globalOutbreak)
	'''
	This function creates a new reading record in the database
	based on the passed in reading data
	:param globalreading:  Global reading record to create in the database
	:return:        200 on success
	'''
	source = globalOutbreak.get('source', None)
	timestamp = globalOutbreak.get('timestamp', None)

	conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='readings'
	)

	c = conn.cursor()	
	sql = "INSERT INTO outbreaks (source, timestamp) VALUES('{}', '{}')".format(source, timestamp)
	print(sql)
	c.execute(sql)
	conn.commit()
	conn.close()

	return make_response('Global outbreak record successfully created', 200)
