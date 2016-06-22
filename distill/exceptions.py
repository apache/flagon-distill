class Error (Exception):
    """Base class for exceptions."""
    pass

class ValidationError (Error):
	""" Exceptions raised for errors in validated a url."""

	def __init__ (self, url, msg):
		self.url = url
		self.msg = msg
