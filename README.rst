==================================================================
distill: An analytical framework for User-ALE <https://github.com/draperlaboratory/user-ale>.
==================================================================

Installation
------------

The easiest way to install most Python packages is via ``easy_install`` or ``pip``::

    $ easy_install distill

Development and Testing
------------

To build the source code and run all unit tests::

    $ python setup.py develop test

To start up the web server, running on localhost:8090::

    $ dev

Using  ``curl``::

	$ curl -XGET 'http://localhost:8090/app/register' -d '{
		"application_name" : "my_app",
		"version" : "0.1",
		"application_description" : "my test app"
	}'

Usage
-----

TODO: This is a good place to start with a couple of concrete examples of how the package should be used.

The boilerplate code provides a dummy ``main`` function that prints out the word 'Hello'::

    >> from distill import main
    >> main()
    
When the package is installed via ``easy_install`` or ``pip`` this function will be bound to the ``distill`` executable in the Python installation's ``bin`` directory (on Windows - the ``Scripts`` directory).
