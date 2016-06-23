from elasticsearch import Elasticsearch, TransportError
from elasticsearch_dsl import DocType, String, Boolean, Date, Float, Search
from elasticsearch_dsl.query import MultiMatch, Match, Q
from elasticsearch import Elasticsearch, TransportError
from elasticsearch_dsl.connections import connections
from werkzeug.datastructures import ImmutableMultiDict, MultiDict

from flask import jsonify, Markup

from distill import app, es

import datetime
import json
import csv
import StringIO
import yaml
import urllib2

class UserAle (object):
	"""
	Main method of entry to perform segmentation and integration of STOUT's master
	answer table (if STOUT is enabled). Advanced and basic analytics is performed in the
	distill.algorithms.stats and distill.algorithms.graphs module.
	"""

	@staticmethod
	def select (app, app_type=None, params=None):
		"""
		"""
		p = parse_query_parameters (app, app_type, params)
		print p
		# doc = UserAleDoc (meta={"index" : app, "doc_type" : app_type});
		# search = UserAleDoc.search().query ('match', activity="HIDE")

	    # 'q': args.get('q', '{}'),
        # 'fields': args.get('fl', '{}'),
        # 'size': args.get ('size', 100),
        # 'scroll': args.get ('scroll', False),
        # 'filters': request_args.getlist ('fq')
 
  		# Start Search
		s = Search (index=app, doc_type=app_type)

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
		# print(response.hits.total)
		return jsonify (response.to_dict())

	@staticmethod
	def search (app,
				app_type=None,
				filters=list (),
				size=100,
				include="*",
				scroll=None,
				sort_field=None):
		""" 
		Perform a search query.

		:param app: [string] application id (e.g. "xdata_v3")
		:param app_type: [string] name of the application type. If None all application types are searched.
		:param filters: [list of strings] list of filters for a query. 
		:param size: [int] maximum number of hits that should be returned
		:param sort_field: [string] sorting field. Currently supported fields: "timestamp", "date"
		:return: [dict] dictionary with processed results. If STOUT is enabled, STOUT data will be merged with final result.
		"""

		# Need some query builder...
		log_result = es.search (index=app, doc_type=app_type, body=query, fields=filters, size=size)

		stout_result = Stout.getSessions ()

		data = merged_results (log_result, stout_result)
		return data

	"""
	"""
	@staticmethod
	def denoise (app, app_type='parsed', save=False):
		pass

"""
Combine a list of dictionaries together to form one complete dictionary
"""
def merge_dicts (lst):
	dall = {}
	for d in lst:
		dall.update (d)
	return dall

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

# """
# Parsed Docs Class
# meta = {'index' : 'xdata_v3'}
# Defaults to doctype=parsed
# """
# class UserAleParsedDoc (DocType):
# 	timestamp = Date ()

# 	class Meta:
# 		doc_type = 'parsed'

# 	def save (self, ** kwargs):
# 		return super (UserAleParsedDoc, self).save (**kwargs)

# doc = UserAleDoc (meta={"index" : "xdata_v3", "doc_type" : "testing"});
# search = UserAleDoc.search().query ('match', activity="HIDE")
