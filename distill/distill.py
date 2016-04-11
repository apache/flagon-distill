from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# from userale import Ale

# configuration - needs to be in a seperate file
ES = 'http://localhost:9200'
DEBUG = True
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)

"""
Show Distill version information, connection status (USERALE), etc.
"""
@app.route ('/')
def index ():
    return 'Index Page'

"""
curl -XPOST https://[hostname]/app -d 
{
    "app_name" : "application_name",
    "description" : "the description of the application",
    "version" : 1.0
}

Creates an index in Elasticsearch to store user logs to
"""
@app.route ('/app/register', methods=['POST'])
def create ():
	print request.form
	return 'Registering application called %s ' % app_id

"""
curl -XGET http://localhost:5000/app/xdata_test -d '{ "version" : 1.0 }
"""
@app.route ('/app/<app_id>', methods=['GET'])
def read (app_id):
	return 'Returning application information stored in Elasticsearch for %s ' % app_id

@app.route ('/app/<app_id>', methods=['PUT'])
def update (app_id):
	return "Updating application %s " % app_id

@app.route ('/app/<app_id>', methods=['DELETE'])
def delete (app_id):
	return 'Deleting application and all data for %s ' % app_id


if __name__ == '__main__':
    app.run (debug=DEBUG)

