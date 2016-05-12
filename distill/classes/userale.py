'''
distill: This package contains a flask app RESTful api for distill

This flask app exposes some restful api endpoints for querying User-ALE. 
Very similar to Lucene syntax for basic query operations.

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from elasticsearch_dsl import DocType, String, Boolean, Date, Float, Search
from elasticsearch import Elasticsearch, TransportError
from elasticsearch_dsl.connections import connections
from datetime import datetime
from flask import jsonify

from distill import my_app, es
import json, yaml, urllib2

"""
Generic class supporting basic CRUD operations
"""
class UserAle (object):

	"""
	Register a new application in User Ale
	Example:
	{
		"application" : "xdata_v3",
		"health" : "green",
		"num_docs" : 0,
		"status" : "open"
	}
	"""
	@staticmethod
	def create (app):
		try:
			res = es.indices.create (index=app)
			doc = get_cluster_status (app)	
			return jsonify (doc)
		except TransportError as e:
			return jsonify (error=e.info)

	"""
	Fetch meta data associated with an application
	Data will include all document types in index and all fields in index
	Example: 
	{
		"application" : "xdata_v3",
		"health" : "green",
		"num_docs" : "100",
		"status" : "open"
		"types" : {
			"raw_logs" : {
				"@timestamp" : "date",
				"action" : "string",
				"elementId" : "string"	
			},
			"parsed" : {
				"@timestamp" : "date",
				"elementId_interval" : "string"
			},
			"graph" : {
				"uniqueID" : "string",
				"transition_count" : "long",
				"p_value" : "float"
			}
		}
	}
	"""
	@staticmethod
	def read (app):
		doc = get_cluster_status (app)
		return jsonify (doc)

	"""
	@TODO Not Implemented
	"""
	@staticmethod
	def update (app):
		return jsonify (status="not implemented")

	"""
	Delete an application from User Ale
	Example: 
	{

	}
	"""
	@staticmethod
	def delete (app):
		try:
			res = es.indices.delete (index=app)
			return jsonify (status="Deleted index %s" % app)
		except TransportError as e:
			return jsonify (e.info)

	"""
	"""
	@staticmethod
	def select (app, type=None, params=None):
		p = parse_query_parameters (app, params)
		pass

	"""
	"""
	@staticmethod
	def denoise (app, doc_type='parsed', save=False):
		pass

"""
Helper method to gather cluster information
"""
def get_cluster_status (app):
	# Return cluster status, index health, and document count as string
	doc = {}
	try:
		cluster_status = es.cat.indices (index=app, h=["health", "status", "docs.count"], pri=True)
		v = str (cluster_status).split (" ")
		m = ["health", "status", "num_docs"]
		doc = dict (zip (m, v))
		# Add back application
		doc ["application"] = app
	except TransportError as e:
		doc ['error'] = e.info
	return doc

"""
Combine a list of dictionaries together to form one complete dictionary
"""
def merge_dicts (lst):
	dall = {}
	for d in lst:
		dall.update (d)
	return dall

"""
@TODO Reformat mapping data
"""
def parse_mappings (app):
	try:
		mappings = es.indices.get_mapping (index=app)
		mappings = yaml.safe_load (json.dumps (mappings))
		# print json.dumps (mappings [app]["mappings"], indent=4, separators=(',', ': '))
		ignore = ["properties", "format"]
	except TransportError as e:
		doc ['error'] = e.info
	return doc

"""
Retrieve all possible columns in app
"""
def get_all_fields (app):
	return []

"""
Get query parameters from the request and preprocess them.
:param [dict-like structure] Any structure supporting get calls
:result [dict] Parsed parameters
"""
def parse_query_parameters(indx, request_args):
    args = {key: value[0] for (key, value) in dict (request_args).iteritems()}

    # Parse out simple filter queries
    filters = []
    for filter in get_all_fields (indx):
        if filter in args:
            filters.append((filter, args[filter]))

    return {
        'q': args.get('q', '{}'),
        'fields': args.get('fl', '{}'),
        'size': args.get ('size', 100),
        'scroll': args.get ('scroll', False),
        'filters': filters
    }

"""
Simple UserAleDoc class to perform queries on index
"""	
class UserAleDoc (DocType):
	pass

# doc = UserAleDoc (meta={"index" : "xdata_v3", "doc_type" : "testing"});
# search = UserAleDoc.search().query ('match', activity="HIDE")

# search = Search (index="xdata_v3").query ()
# search = search[:20]

# response = search.execute()

# print(response.hits.total)
# print(response[0].activity)