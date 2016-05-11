from elasticsearch_dsl import DocType, String, Boolean, Date, Float, Search
from elasticsearch import Elasticsearch, TransportError
from elasticsearch_dsl.connections import connections
from datetime import datetime
from distill import my_app
import json, yaml, urllib2

# Unpack Elasticsearch configuration and create elasticsearch connection
host = my_app.config ['ES_HOST']
port = my_app.config ['ES_PORT']
http_auth = my_app.config ['HTTP_AUTH']
use_ssl = my_app.config ['USE_SSL']
verify_certs = my_app.config ['VERIFY_CERTS']
ca_certs = my_app.config ['CA_CERTS']
client_cert = my_app.config ['CLIENT_CERT']
client_key = my_app.config ['CLIENT_KEY']

# Global connection 
es = connections.create_connection (hosts = [host], \
								   	port = port, \
								   	http_auth = http_auth, \
								   	use_ssl = use_ssl, \
								   	verify_certs = verify_certs,
								   	ca_certs = ca_certs, \
								   	client_cert = client_cert, \
								   	client_key = client_key)

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
			res = yaml.safe_load (json.dumps (res))	
			doc = get_cluster_status (app)	
		except TransportError as e:
			doc = e.info
		return json.dumps (doc, indent=4, separators=(',', ': '), sort_keys=True)

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
		# Final Result to return to Client
		doc = get_cluster_status (app)

		return json.dumps (doc, indent=4, separators=(',', ': '), sort_keys=True)

	"""
	@TODO Not Implemented
	"""
	@staticmethod
	def update (app):
		return "True"

	"""
	Delete an application from User Ale
	Example: 
	{

	}
	"""
	@staticmethod
	def delete (app):
		res = es.indices.delete (index=app)
		return res

"""
Helper method to gather cluster information
"""
def get_cluster_status (app):
	# Return cluster status, index health, and document count as string
	doc = {}
	try:
		cluster_status = es.cat.indices (index=app, h=["health", "status", "docs.count"], pri=True)
		print "help!"
		v = str (cluster_status).split (" ")
		m = ["health", "status", "num_docs"]
		doc = dict (zip (m, v))
		# Add back application
		doc ["application"] = app
	except TransportError as e:
		doc = e.info
	return doc

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
		pass
	return 

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