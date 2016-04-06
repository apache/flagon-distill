from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from userale import Ale

# configuration
ES = 'http://localhost:9200'
DEBUG = True
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)

@app.route ('/')
def index ():
    return 'Index Page'

@app.route ('/app/<app_id>', methods=['POST'])
def create (app_id):
	return 'Registering application called %s ' % app_id

@app.route ('/app/<app_id>', methods=['GET'])
def read (app_id):
	return 'Returning application information stored in Elasticsearch for %s ' % app_id

@app.route ('/app/<app_id>', methods=['POST'])
def update (app_id):
	return "Updating application %s " % app_id

@app.route ('/app/<app_id>', methods=['DELETE'])
def delete (app_id):
	return 'Deleting application and all data for %s ' % app_id


if __name__ == '__main__':
    app.run (debug=DEBUG)

