'''
distill: This package contains a flask app RESTful api for distill

This flask app exposes some restful api endpoints for querying User-ALE. 
Very similar to Lucene syntax for basic query operations.

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from flask import Flask, request, jsonify
from distill import my_app
from distill.classes.userale import UserAle
from distill.exceptions import ValidationError
from distill.validation import validate_request

"""
curl -XGET https://[hostname]:[port]

Show Distill version information, connection status, number of live nodes/shards, etc.
"""
@my_app.route ('/', methods=['GET'])
def index ():	
	return jsonify (name="Distill", version="1.0 alpha", author="Michelle Beard", email="mbeard@draper.com")

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
@my_app.route ('/<app_id>/select', defaults={"app_type": None})
@my_app.route ('/<app_id>/<app_type>/select', methods=['GET'])
def select (app_id, app_type):
	q = request.args
	try:
		validate_request (q)
		return UserAle.select (app_id, type=app_type, params=q)
	except ValidationError as e:
		return jsonify (error=e.message)

"""
curl -XGET http://[hostname]:[port]/app_name/denoise?save=true&type=parsed

Run the denoise script to cleanup the raw logs. A document type called "parsed"
will be stored with new log created unless specified in the request. Have option to save 
parsed results back to data store.
"""
@my_app.route ('/<app_id>/denoise', methods=['GET'])
def denoise (app_id):
	doc_type = 'parsed'
	save = False
	q = request.args
	if 'save' in q:
		save = str2bool (q.get ('save'))
	if 'type' in q:
		"""
		@TODO: Proper cleanup script needs to happen
		"""
		doc_type = q.get ('type')
	return UserAle.denoise (app_id, doc_type=doc_type, save=save)

"""
@TODO
"""
@my_app.route ('/<app_id>/update', methods=['POST'])
def update (app_id):
	return UserAle.update (app_id)

"""
Generic Error
"""
@my_app.errorhandler(404)
def page_not_found (error):
	return "Unable to find Distill." 
