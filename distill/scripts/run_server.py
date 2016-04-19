'''
distill: Development Server scripts.

Copyright 2016, The Charles Stark Draper Laboratory, Inc.
Licensed under Apache Software License
'''

from distill import my_app
from distill.app import *

"""
@TODO
Define Distill production server
"""
def run_server ():
	print "production server yet defined"

"""
Devlopment server
"""
def dev_server ():
	host = my_app.config ['HOST']
	port = my_app.config ['PORT']
	debug = my_app.config ['DEBUG']
	my_app.run (host=host, port=port, debug=debug)

if __name__ == '__main__':
    dev_server ()
