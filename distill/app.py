'''
distill: This package contains a flask app RESTful api for distill

This flask app exposes some restful api endpoints for querying User-ALE. 
Very similar to Lucene syntax for basic query operations.

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from flask import Flask, request, jsonify
from distill import app
from distill.classes.userale import UserAle
from distill.classes.stout import Stout
from distill.exceptions import ValidationError
from distill.validation import validate_request

"""
curl -XGET https://[hostname]:[port]

Show Distill version information, connection status, number of live nodes/shards, etc.
"""
@app.route ('/', methods=['GET'])
def index ():	
	return jsonify (name="Distill", version="1.0 alpha", author="Michelle Beard", email="mbeard@draper.com", status=UserAle.getStatus ())

"""
curl -XPOST https://[hostname]:[port]/create/app_name
curl -XPUT https://[hostname]:[port]/create/app_name

Example:
curl -XPOST https://[hostname]:[port]/xdata_v3
curl -XPUT https://[hostname]:[port]/xdata_v3

Creates an index in Elasticsearch to store user logs to
"""
@app.route ('/create/<app_id>', defaults={"app_id" : False}, methods=['POST', 'PUT'])
def create (app_id):
	return UserAle.create (app_id)

"""
curl -XGET https://[hostname]:[port]/status/app_name

Example:
curl -XGET https://[hostname]:[port]/status/xdata_v3

Presents meta information about index app_name: field names and document types
"""
@app.route ('/status/<app_id>', defaults={"app_id" : False}, methods=['GET'])
def status (app_id): 
	return UserAle.read (app_id)

"""
@TODO
"""
@app.route ('/update/<app_id>', methods=['POST'])
def update (app_id):
	return UserAle.update (app_id)

"""
curl -XDELETE https://[hostname]:[port]/app_name

curl -XDELETE https://[hostname]:[port]/xdata_v3

Deletes an index permentantly from Elasticsearch
"""
@app.route ('/delete/<app_id>', defaults={"app_id" : False}, methods=['DELETE'])
def delete (app_id):
	return UserAle.delete (app_id)

"""
curl -XGET http://[hostname]:[port]/app_name/select?q=*:*&size=100&scroll=true&fl=param1,param2

Example:
curl -XGET http://[hostname]:[port]/app_name/select?q=session_id:A1234&size=100&scroll=false&fl=param1,param2

Get all data associated with an application
""" 
@app.route ('/search/<app_id>', defaults={"app_type" : None})
@app.route ('/search/<app_id>/<app_type>', methods=['GET'])
def search (app_id, app_type):
	q = request.args
	try:
		validate_request (q)
		return UserAle.select (app_id, app_type=app_type, params=q)
	except ValidationError as e:
		return jsonify (error=e.message)

"""
curl -XGET http://[hostname]:[port]/denoise/app_name?save=true&type=parsed

Bootstrap script to cleanup the raw logs. A document type called "parsed"
will be stored with new log created unless specified in the request. Have option to save 
parsed results back to data store. These parsed logs can be intergrated with STOUT results 
by running the stout bootstrap script 
"""
@app.route ('/denoise/<app_id>', methods=['GET'])
def denoise (app_id):
	doc_type = 'parsed'
	save = False
	q = request.args
	if 'save' in q:
		save = str2bool (q.get ('save'))
	if 'type' in q:
		# @TODO: Proper cleanup script needs to happen
		doc_type = q.get ('type')
	return UserAle.denoise (app_id, doc_type=doc_type, save=save)

"""
Bootstrap script to aggregate user ale logs to stout master answer table
This will save the merged results back to ES instance at new index stout
OR denoise data first, then merge with the stout index...
If STOUT is enabled, the select method expects a stout index to exist or otherwise 
it will return an error message. 
"""
@app.route ('/stout/<app_id>', defaults={"app_type" : None})
@app.route ('/stout/<app_id>/<app_type>', methods=['GET'])
def merge_stout (app_id):
	pass

"""
Generic Error Message
"""
@app.errorhandler(404)
def page_not_found (error):
	return "Unable to find Distill." 
