from flask import Flask
from flask_mysql_connector import MySQL
import os 
from configparser import ConfigParser

app = Flask(__name__)

config = ConfigParser()
path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config.read(os.path.join(path, 'database_config.ini'))
database_config = config['database_config']

app.config['MYSQL_USER'] = database_config['MYSQL_USER']
app.config['MYSQL_DATABASE'] = database_config['MYSQL_DB']
app.config['MYSQL_HOST'] = database_config['HOST']
app.config['MYSQL_PASSWORD'] = database_config['MYSQL_PASSWORD']
app.config['MYSQL_PORT'] = database_config['MYSQL_PORT']
app.config['MYSQL_AUTH_PLUGIN'] = database_config['MYSQL_AUTH_PLUGIN']

mysql = MySQL(app)

EXAMPLE_SQL = 'select * from Reddit.Comment'

@app.route('/connection')
def connection():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(EXAMPLE_SQL)
    output = cur.fetchall()
    return str(output)



if __name__ == '__main__':
    app.run(debug=True)