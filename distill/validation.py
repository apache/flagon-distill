'''
distill: This package contains a flask app RESTful api for distill

This flask app exposes some restful api endpoints for querying User-ALE. 
Very similar to Lucene syntax for basic query operations.

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from distill.exceptions import ValidationError
import json, yaml

# doc = yaml.safe_load (msg)
# 	return json.dumps (doc, indent=4, separators=(',', ': '), sort_keys=True)


"""
Raises ValidationError 
"""
def validate_request (q):
	if 'q' not in q:
		raise ValidationError ("Missing required parameter: %s" % 'q')
	else:
		# Handle rest of parsing
		pass

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")