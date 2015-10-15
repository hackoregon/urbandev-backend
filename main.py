# Web app imports
import flask
from flask import Flask, send_from_directory
from flask.ext.mysqldb import MySQL

# Out config
import consts
from config import kMySQLSettings

# Utilities
from util import genMarkdownResult


## Web app config
app = Flask(__name__)
app.config['DEBUG'] = consts.DEBUG_APP

# Database connection
app.config['MYSQL_HOST'] = kMySQLSettings['host']
app.config['MYSQL_USER'] = kMySQLSettings['user']
app.config['MYSQL_PASSWORD'] = kMySQLSettings['pwd']
app.config['MYSQL_DB'] = kMySQLSettings['dbname']
app.config['MYSQL_PORT'] = kMySQLSettings['port']
app.config['MYSQL_USE_UNICODE'] = True
app.config['MYSQL_CHARSET'] = 'utf8'

# Cache DB connection factory in global
app.config['DBCONN'] = MySQL(app)

# Pretty print JSON responses only if debugging
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = consts.DEBUG_APP



# Routes in other modules
import permits, neighborhoods, taxlots, crimes, census


# URL map - one per service
urlMap = [
   ('/permits', permits.permits_api),
   ('/permits<ext>', permits.permits_api),
   ('/neighborhoods', neighborhoods.neighborhoods_api),
   ('/taxlots', taxlots.taxlots_api),
   ('/crimes', crimes.crimes_api),
   ('/census', census.census_api)
]

for url in urlMap:
   app.add_url_rule(url[0], view_func=url[1])


@app.route('/')
def index():
    return genMarkdownResult("doc/services.md")

@app.route('/demo')
def demo():
    return open('./demo.html', 'r').read()
  
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('doc', path)
    
    
# Bootstrap the application server
if __name__ == '__main__':
    app.run()


