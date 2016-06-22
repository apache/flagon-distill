from distill.exceptions import ValidationError

def validate_request (q):
	""" 
	Parse out request message and validate inputs

	:param q: Url query string
	:raises ValidationError: if the query is missing required parameters
	"""
	if 'q' not in q:
		raise ValidationError ("Missing required parameter: %s" % 'q')
	else:
		# Handle rest of parsing
		pass

def str2bool (v):
	"""
	Convert string expression to boolean

	:param v: Input value
	:returns: Converted message as boolean type
	:rtype: bool
	"""
	return v.lower() in ("yes", "true", "t", "1")