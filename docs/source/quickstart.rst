.. _quickstart:

Quickstart Guide
================

Usage
-----

Using  ``curl``::

	$ curl -XGET 'http://localhost:8090/app/register' -d '{
		"application_name" : "my_app",
		"version" : "0.1",
		"application_description" : "my test app"
	}'