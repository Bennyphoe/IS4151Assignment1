import mysql.connector
from flask import make_response

conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='readings',
  		autocommit = True
)

def read():

	c = conn.cursor()
	c.execute('SELECT * FROM outbreaks')
	results = c.fetchall()

	
	return results



def create(payload):
	print(payload)
	'''
	This function creates a new reading record in the database
	based on the passed in reading data
	:param globalreading:  Global reading record to create in the database
	:return:        200 on success
	'''
	source = payload.get('source', None)
	timestamp = payload.get('timestamp', None)

	c = conn.cursor()	
	sql = "INSERT INTO outbreaks (source, timestamp) VALUES('{}', '{}')".format(source, timestamp)
	print(sql)
	c.execute(sql)
	conn.commit()

	return make_response('Global outbreak record successfully created', 200)

def update(status, id):
	c = conn.cursor()
	sql = 'UPDATE outbreaks SET status = "{}" WHERE id = {}'.format(status, id)
	c.execute(sql)
	conn.commit()
	return make_response('Global outbreak record Updated status successfully', 200)