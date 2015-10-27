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
import permits, neighborhoods, taxlots, crimes, census, demolitions


# URL map - one or more per service
urlMap = [
   ('/permits', '/permits.<fileext>', permits.permits_api),
   ('/neighborhoods', '/neighborhoods.<fileext>', neighborhoods.neighborhoods_api),
   ('/taxlots', taxlots.taxlots_api),
   ('/crimes', '/crimes.<fileext>', crimes.crimes_api),
   ('/census', census.census_api),
   ('/demolitions', '/demolitions.<fileext>', demolitions.demolitions_api)
]

# Load urls - permit multiple route names for a single view
for url in urlMap:
   for ul in url[:-1]:
      app.add_url_rule(ul, view_func=url[-1])


@app.after_request
def after_request(response):
    '''Add CORS headers to API requests. These headers are returned with every request (including OPTIONS)'''
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response
  
  
@app.route('/')
def index():
    return genMarkdownResult("doc/services.md")

@app.route('/demo')
def demo():
    return open('./demo.html', 'r').read()
  
# CSS for markdown docs
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('doc', path)
    
# JS for demo / test app
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
    
    
# Bootstrap the application server
if __name__ == '__main__':
    app.run()


