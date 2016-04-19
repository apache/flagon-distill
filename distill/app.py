'''
distill: This package contains a flask app RESTful api for distill

This flask app exposes some restful api endpoints for querying User-ALE. 

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from flask import Flask, request
from distill import my_app

"""
Show Distill version information, connection status (USERALE), etc.
"""
@my_app.route ('/')
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
@my_app.route ('/app/register', methods=['POST'])
def create ():   
	return 'Registering application called %s ' % app_id

"""
curl -XGET http://localhost:5000/app/xdata_test -d '{ "version" : 1.0 }
"""
@my_app.route ('/app/<app_id>', methods=['GET'])
def read (app_id):
	return 'Returning application information stored in Elasticsearch for %s ' % app_id

@my_app.route ('/app/<app_id>', methods=['PUT'])
def update (app_id):
	return "Updating application %s " % app_id

@my_app.route ('/app/<app_id>', methods=['DELETE'])
def delete (app_id):
	return 'Deleting application and all data for %s ' % app_id

@my_app.errorhandler(404)
def page_not_found (error):
	return "Unable to find Distill." 