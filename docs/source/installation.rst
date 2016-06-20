.. _installation:

Installing Distill
==================

The first step to getting going is installing Distill. Distill is a python project, so it can be installed like any other python library. Several Operating Systems (Mac OS X, Major Versions of Linux/BSD) have Python pre-installed, so you should just have to run::

    $ easy_install distill

Advanced users can install this in a virtualenv if they wish. 

When the package is installed via ``easy_install`` or ``pip`` this function will be bound to the ``distill`` executable in the Python installation's ``bin`` directory (on Windows - the ``Scripts`` directory).

Development and Testing
-----------------------

To build the source code and run all unit tests::

    $ python setup.py develop test

To start up a local web server, running on localhost:8090::

    $ dev


Distill Deployment
------------------

I will describe a setup with nginx as a web server on Ubuntu. A web server cannot communicate directly with a Flask application such as Distill, that’s why gunicorn will be used to act as a medium between the web server and Distill. Gunicorn is like an application web server that will be running behind nginx, and it is WSGI compatible. It can communicate with applications that support WSGI – Flask, Django, etc.

Install requirements::

	$ sudo apt-get update
	$ sudo apt-get install -y python python-pip nginx gunicorn

Create a directory to store the project::

	$ sudo mkdir /home/pubic_html && cd /home/public_html

Download the project from the GitHub repository and copy the application to the home/www directory::

	$ git clone https://github.com/draperlaboratory/distill.git /home/public_html

Install Distill's requirements::

	$ pip install -r requirements.txt

Distill has provided an nginx configuration file located in ``distill/deploy/nginx.conf``.

Gunicorn will use port 8000 and handle the incoming HTTP requests.

Restart nginx to load the configuration changes::

	$ sudo /etc/init.d/nginx restart

Run gunicorn on port 8000::

	$ gunicorn --workers 4 --bind unix:distill.sock -m 007 deploy/run_server:app 

Start a new browser instance and navigate to::

	$ http://server_address

Building Documentation 
----------------------

To build Distill's documentation::

	$ python setup.py build_sphinx

Or::

	# Inside top-level docs/ directory.
 	$ make html

This should build the documentation in your shell, and output HTML. At then end, it should say something about documents being ready in _build/html. 
You can now open them in your browser by typing::

	$ open _build/html/index.html