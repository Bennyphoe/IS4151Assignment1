import connexion
import mysql.connector



app = connexion.App(__name__, specification_dir='./')
app.add_api('cloud.yml')



@app.route('/')
def index():

	conn = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='password',
		database='readings'
	)
	
	c = conn.cursor()
	c.execute('SELECT devicename, AVG(temp) AS averagetemp, AVG(lightlevel) AS averageLightLevel FROM readings GROUP BY devicename ORDER BY devicename ASC')
	results = c.fetchall()
	
	html = '<html><head><title>Cloud Server</title></head><body><h1>Global Temperatures</h1><table cellspacing="1" cellpadding="3" border="1"><tr><th>Device Name</th><th>Average Temperature</th><th>Average Light level</th></tr>'
	for result in results:
				
		html += '<tr><td>' + result[0] + '</td><td>' + str(result[1]) + '</td><td>' + str(result[2]) + '</td></tr>'
	
	html += '</body></html>'
	
	conn.close()
	
	return html

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
