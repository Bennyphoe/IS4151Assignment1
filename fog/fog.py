import sqlite3
from flask import Flask, render_template



app = Flask(__name__, template_folder='../templates', static_folder="../static" )



@app.route('/')
def index():

	conn = sqlite3.connect('readings.db')
	c = conn.cursor()
	c.execute('SELECT devicename, temp, lightlevel FROM readings ORDER BY devicename ASC')
	results = c.fetchall()
	c.execute('SELECT source, timestamp, tocloud FROM outbreaks')	
	outbreaks = c.fetchall()
	conn.close()
	
	return render_template('fog.html', readings = results, outbreaks = outbreaks)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
