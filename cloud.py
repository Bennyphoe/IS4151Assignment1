import connexion
import mysql.connector
from flask import Flask, render_template



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
    
    c.execute('SELECT source, timestamp, status FROM outbreaks')
    outbreaks = c.fetchall()
    conn.close()
	
    return render_template('cloud.html', readings = results, outbreaks = outbreaks)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
