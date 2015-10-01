# Web app imports
import flask
from flask import Flask
from flask.ext.mysqldb import MySQL

from config import kMySQLSettings

# Web app config
app = Flask(__name__)
app.config['DEBUG'] = True

app.config['MYSQL_HOST'] = kMySQLSettings['host']
app.config['MYSQL_USER'] = kMySQLSettings['user']
app.config['MYSQL_PASSWORD'] = kMySQLSettings['pwd']
app.config['MYSQL_DB'] = kMySQLSettings['dbname']
app.config['MYSQL_PORT'] = kMySQLSettings['port']
app.config['MYSQL_USE_UNICODE'] = True
app.config['MYSQL_CHARSET'] = 'utf8'

app.config['DBCONN'] = MySQL(app)


# Utilities
from util import genMarkdownResult

# Routes in other modules
import permits, neighborhoods, taxlots, crimes


# URL map - one per service
app.add_url_rule('/permits', view_func=permits.permits)
app.add_url_rule('/neighborhoods', view_func=neighborhoods.neighborhoods)
app.add_url_rule('/taxlots', view_func=taxlots.taxlots)
app.add_url_rule('/crimes', view_func=crimes.crimes)



@app.route('/')
def index():
    return genMarkdownResult("doc/services.md")

  

# Bootstrap the application server
if __name__ == '__main__':
    app.run()


