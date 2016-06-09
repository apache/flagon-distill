'''
distill: This package contains a flask app RESTful api for distill

This flask app exposes some restful api endpoints for querying User-ALE. 
Very similar to Lucene syntax for basic query operations.

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from distill import app
import sqlite3
import pandas as pd

class Stout ():
	conn = None
	cursor = None

	"""
	Parse master answer table into readable/queryable format
	"""
	def parse (f):
		pass

	def connect ():
		# Load Configurations
		app.config.from_pyfile('config.cfg')
		db = app.config ['SQLITEDB']
		conn = sqlite3.connect (db)
		cursor = conn.cursor ()

	def lookup (topic='SYS_IND_SESS_'):
		cursor.execute ('SELECT ' + topic + ' FROM stout')

	def operational_task (sessionID=''):
		pass
		# Look up session ID : tasknum in DB
		# Determine if performing task1 or task2
		# Add new column OT 
