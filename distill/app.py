'''
distill: This package contains a flask app RESTful api for distill

This flask app exposes some restful api endpoints for querying User-ALE. 
Very similar to Lucene syntax for basic query operations.

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from flask import Flask, request
from distill import my_app
from distill.classes.userale import UserAle
import json

"""
curl -XGET https://[hostname]:[port]

Show Distill version information, connection status, number of live nodes/shards, etc.
"""
@my_app.route ('/', methods=['GET'])
def index ():	
	msg = '{ "name" : "Distill", "version": "1.0 alpha", "author" : "Michelle Beard <mbeard@draper.com>" }'
	# parsed = json.loads (msg)
	# print parsed
	# res = json.dumps (parsed, sort_keys=True, indent=4, separators=(',',':'))
	# print res
	return msg

"""
curl -XGET https://[hostname]:[port]/app_name
curl -XPOST https://[hostname]:[port]/app_name
curl -XDELETE https://[hostname]:[port]/<app_id>

Example:
curl -XGET https://[hostname]:[port]/xdata_v3
curl -XPOST https://[hostname]:[port]/xdata_v3
curl -XDELETE https://[hostname]:[port]/xdata_v3

If GET: Presents meta information about index app_name: field names and document types
If POST/PUT: Creates an index in Elasticsearch to store user logs to
If DELETE: Deletes an index permentantly from Elasticsearch
"""
@my_app.route ('/<app_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def register (app_id): 
	if request.method == 'GET':
		return UserAle.read (app_id)
	elif request.method == 'POST' or request.method == 'PUT':
		return UserAle.create (app_id)
	elif request.method == 'DELETE':
		return UserAle.delete (app_id)
	else:
		return UserAle.read (app_id)

"""
curl -XGET http://[hostname]:[port]/app_name/select?q=*:*&size=100&scroll=true&fl=param1,param2

Example:
curl -XGET http://[hostname]:[port]/app_name/select?q=session_id:A1234&size=100&scroll=false&fl=param1,param2

Get all data associated with an application
"""
@my_app.route ('/<app_id>/select', methods=['GET'])
def select (app_id):
	error = None
	# Parsing parameters
	# required q
	# optional: everything else
	required = ["q"]
	optional = ["size", "scroll", "fl"]

@my_app.route ('/<app_id>/<app_type>/select', methods=['GET'])
def query (app_id, app_type):
	return "false"
"""
@TODO
"""
@my_app.route ('/<app_id>/update', methods=['POST'])
def update (app_id):
	return UserAle.update (app_id)

"""
Error handling
"""
@my_app.errorhandler(404)
def page_not_found (error):
	return "Unable to find Distill." 
