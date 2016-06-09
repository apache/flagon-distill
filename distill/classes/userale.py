'''
distill: This package contains a flask app RESTful api for distill

This flask app exposes some restful api endpoints for querying User-ALE. 
Very similar to Lucene syntax for basic query operations.

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from elasticsearch_dsl import DocType, String, Boolean, Date, Float, Search
from elasticsearch_dsl.query import MultiMatch, Match, Q
from elasticsearch import Elasticsearch, TransportError, ConnectionError
from elasticsearch_dsl.connections import connections
from werkzeug.datastructures import ImmutableMultiDict, MultiDict

from flask import jsonify, Markup

from distill import app, es

import datetime
import json
import yaml
import urllib2

"""
Generic class supporting basic CRUD operations
"""
class UserAle (object):

	@staticmethod
	def getStatus ():
		"""
		Get Status of Elasticsearch Instance
		"""
		try:
			res = es.ping ()
		except ConnectionError as e:
			res = False
		return res

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
		# try:
		# 	res = es.indices.delete (index=app)
		# 	return jsonify (status="Deleted index %s" % app)
		# except TransportError as e:
		# 	return jsonify (e.info)
		return jsonify (status="not allowed")

	"""
	Main method of entry to perform segmentation and integration of STOUT's master
	answer table (if STOUT is enabled). 
	"""
	@staticmethod
	def select (app, app_type=None, params=None):
		p = parse_query_parameters (app, app_type, params)
		# doc = UserAleDoc (meta={"index" : app, "doc_type" : app_type});
		# search = UserAleDoc.search().query ('match', activity="HIDE")

	    # 'q': args.get('q', '{}'),
        # 'fields': args.get('fl', '{}'),
        # 'size': args.get ('size', 100),
        # 'scroll': args.get ('scroll', False),
        # 'filters': request_args.getlist ('fq')
 
  		# Start Search
		s = Search (index="xdata_v3", doc_type=app_type)

		# Check query


		# Execute Filter Query
		for x in p['filters']:
			l = x.split (':', 1)
			m = {}
			m[l[0]] = l[1]

			# print m[l[0]]
			s = s.query ('match', **m)

		# Check fields array
		fields = p ['fields']
		# if not fields:
		# Comma delimited list
		s = s.fields (p['fields'])

		# Filter request
		# s = s.filter('terms', tags='5c8b88fbca0fc7a5783c77931e037d\:\:3139')

		# Size

		# Execute
		response = s.execute()
		print(response.hits.total)
		return jsonify (response.to_dict())

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
def parse_mappings (app, app_type=None):
	try:
		mappings = es.indices.get_mapping (index=app, doc_type=[app_type])
		# mappings = yaml.safe_load (json.ess (mappings))
		# print json.dumps (mappings [app]["mappings"], indent=4, separators=(',', ': '))
		ignore = ["properties", "format"]
	except TransportError as e:
		doc ['error'] = e.info
	return doc

"""
Retrieve all possible columns in app
"""
def get_all_fields (app, app_type=None):
    # mappings = es.indices.get_mapping (index=app, doc_type=app_type)
    # mappings = json.loads (mappings)
    # data = {key: value for (key, value) in dict(mappings).items ()}
    # print mappings
    return ['sessionID']

"""
Get query parameters from the request and preprocess them.
:param [dict-like structure] Any structure supporting get calls
:result [dict] Parsed parameters
"""
def parse_query_parameters (indx, app_type=None, request_args = {}):
    args = {key: value[0] for (key, value) in dict (request_args).iteritems ()}

    # print "args = ", args
    # Parse out simple filter queries
    filters = []
    for filter in get_all_fields (indx, app_type):
        if filter in args:
            filters.append((filter, args[filter]))
    
    return {
        'q': args.get('q', '{}'),
        'fields': args.get('fl', []),
        'size': args.get ('size', 100),
        'scroll': args.get ('scroll', False),
        'filters': request_args.getlist ('fq')
    }

"""
Parsed Docs Class
meta = {'index' : 'xdata_v3'}
Defaults to doctype=parsed
"""
class UserAleParsedDoc (DocType):
	timestamp = Date ()

	class Meta:
		doc_type = 'parsed'

	def save (self, ** kwargs):
		return super (UserAleParsedDoc, self).save (**kwargs)

# doc = UserAleDoc (meta={"index" : "xdata_v3", "doc_type" : "testing"});
# search = UserAleDoc.search().query ('match', activity="HIDE")
