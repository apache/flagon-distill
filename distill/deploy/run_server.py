'''
distill: Development Server scripts.

Copyright 2016, The Charles Stark Draper Laboratory, Inc.
Licensed under Apache Software License
'''

from distill import app
from distill.app import *

"""
Start up a local WSGI server called development 
"""
def dev_server ():
	host = app.config ['HOST']
	port = app.config ['PORT']
	debug = app.config ['DEBUG']
	app.run (host=host, port=port, debug=debug)

if __name__ == '__main__':
    dev_server ()
