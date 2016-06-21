__license__ = "Apache-2.0"
__revision__ = " $Id:  $ "
__docformat__ = 'reStructuredText'

from flask import Flask, request, jsonify
from distill import app
from distill.models.userale import UserAle
from distill.models.stout import Stout
from distill.exceptions import ValidationError
from distill.validation import validate_request


@app.route ('/', methods=['GET'])
def index ():	
	"""
	Show Distill version information, connection status, and all registered applications.

	.. code-block:: bash
	
		$ curl -XGET https://localhost:8000

		{
			"author" : "Michelle Beard",
			"email" : "mbeard@draper.com",
			"name": "Distill",
			"status" : true,
			"version" : "1.0",
			"apps" : {
				"xdata_v3" : {
					testing: 205,
					parsed: 500,
				},
				"test_app" : {
					logs: 500,
					parsed: 100,
				}
			}
		}

	:return: Distill's status information as JSON blob
	"""
	return jsonify (name="Distill", version="1.0 alpha", author="Michelle Beard", email="mbeard@draper.com", status=UserAle.getStatus (), applications=UserAle.getApps ())

@app.route ('/create/<app_id>', methods=['POST', 'PUT'])
def create (app_id):
	"""
	Registers an application in Distill. 

	.. code-block:: bash

		$ curl -XPOST https://localhost:8000/xdata_v3
	
	:param app_id: Application name
	:return: Newly created application's status as JSON blob
	"""
	return UserAle.create (app_id)

@app.route ('/status/<app_id>', methods=['GET'])
def status (app_id): 
	"""
	Presents meta information about an registered application, including field names and document types.

	.. code-block:: bash

		$ curl -XGET https://localhost:8000/status/xdata_v3

	:param app_id: Application name
	:return: Registered applications meta data as JSON blob
	"""
	return UserAle.read (app_id)

@app.route ('/update/<app_id>', methods=['POST', 'PUT'])
def update (app_id):
	"""
	Renames a specific application 

	.. code-block:: bash

		$ curl -XPOST https://localhost:8000/update/xdata_v3?name="xdata_v4"

	:param app_id: Application name
	:return: Boolean response message as JSON blob
	"""
	return UserAle.update (app_id)

@app.route ('/delete/<app_id>', methods=['DELETE'])
def delete (app_id):
	"""
	Deletes an application permentantly from Distill

	.. code-block:: bash

		$ curl -XDELETE https://localhost:8000/xdata_v3
	
	:param app_id: Application name
	:return: Boolean response message as JSON blob
	"""
	return UserAle.delete (app_id)

@app.route ('/search/<app_id>', defaults={"app_type" : None}, methods=['GET'])
@app.route ('/search/<app_id>/<app_type>', methods=['GET'])
def search (app_id, app_type):
	"""
	Search against an application on various fields.

	.. code-block:: bash

		$ curl -XGET https://[hostname]:[port]/app_name/select?q=session_id:A1234&size=100&scroll=false&fl=param1,param2

	:param app_id: Application name
	:param app_type: Optional document type to filter against
	:param q: Main search query
	:param size: Maximum number of documents to return in request
	:param scroll: Scroll id if the number of documents exceeds 10,000
	:param fl: List of fields to restrict the result set
	:return: JSON blob of result set
	""" 

	q = request.args
	try:
		validate_request (q)
		return UserAle.select (app_id, app_type=app_type, params=q)
	except ValidationError as e:
		return jsonify (error=e.message)

@app.route ('/stat/<app_id>', defaults={"app_type" : None}, methods=['GET'])
@app.route ('/stat/<app_id>/<app_type>', methods=['GET'])
def stat (app_id, app_type):
	"""
	.. warning:: Not implemented/available 

	Generic histogram counts for a single registered application filtered optionally by document type.

	.. code-block:: bash

		$ curl -XGET https://localhost:8000/xdata_v3/testing/?elem=signup&event=click

	:param app_id: Application name
	:param app_type: Application type
	:return: JSON blob of result set
	"""
	q = request.args
	return jsonify (error='Not implemented')

@app.route ('/denoise/<app_id>', methods=['GET'])
def denoise (app_id):
	"""
	Bootstrap script to cleanup the raw logs. A document type called "parsed"
	will be stored with new log created unless specified in the request. Have option to save 
	parsed results back to data store. These parsed logs can be intergrated with STOUT results 
	by running the stout bootstrap script.

	.. code-block:: bash
	
		$ curl -XGET https://localhost:8000/denoise/xdata_v3?save=true&type=parsed

	:param app_id: Application name
	:return: JSON blob of status
	"""
	doc_type = 'parsed'
	save = False
	q = request.args
	if 'save' in q:
		save = str2bool (q.get ('save'))
	if 'type' in q:
		# @TODO: Proper cleanup script needs to happen
		doc_type = q.get ('type')
	return UserAle.denoise (app_id, doc_type=doc_type, save=save)

@app.route ('/stout', methods=['GET'])
def merge_stout ():
	"""
	Bootstrap script to aggregate user ale logs to stout master answer table
	This will save the merged results back to ES instance at new index stout
	OR denoise data first, then merge with the stout index...
	If STOUT is enabled, the select method expects a stout index to exist or otherwise 
	it will return an error message. 

	.. code-block:: bash

		$ curl -XGET https://locahost:8000/stout/xdata_v3

	:return: Status message
	"""
	flag = app.config ['ENABLE_STOUT']
	if flag:
		return Stout.ingest ()
	return jsonify (status="STOUT is disabled.")

@app.errorhandler(404)
def page_not_found (error):
	"""
	Generic Error Message
	"""
	return "Unable to find Distill." 
