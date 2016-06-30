.. _installation:

Installation Guide
==================

Installing Distill
------------------

The first step is to install Distill. First, checkout the latest version of Distill.

::

	$ git clone https://github.com/draperlaboratory/distill.git

Distill is a python project, so it can be installed like any other python library. Several operating systems (Mac OS X, Major Versions of Linux/BSD) have Python pre-installed, so you should just have to run

::
	
    $ easy_install distill

or

::

    $ pip install distill

Users are strongly recommended to install Distill in a virtualenv. Instructions to setup an virtual environment will be explained below.

.. note ::

	When the package is installed via ``easy_install`` or ``pip`` this function will be bound to the ``distill`` executable in the Python installation's ``bin`` directory (on Windows - the ``Scripts`` directory).

Installing Distill in an Virtual Environment
--------------------------------------------

virtualenv is a tool to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that the Distill project would need. 

Install virtualenv via pip:

::

	$ sudo pip install virtualenv

Start by changing directory into the root of Distill's project directory, and then use the virtualenv command-line tool to create a new environment:

::

	$ mkdir env 
	$ virtualenv env

Activate environment:

::

	$ source env/bin/activate

Install Distill requirements:

::

	$ env/bin/pip -r requirements.txt

To build the source code and run all unit tests.

::

    $ env/bin/python setup.py develop test

Launch local Distill server, running on localhost:8090:

::
	
	$ env/bin/dev 

Deactivate environment

:: 	

	$ deactivate

Deployment
----------

I will describe a setup with nginx as a web server on Ubuntu. A web server cannot communicate directly with a Flask application such as Distill, that’s why gunicorn will be used to act as a medium between the web server and Distill. Gunicorn is like an application web server that will be running behind nginx, and it is WSGI compatible. It can communicate with applications that support WSGI – Flask, Django, etc.

Install requirements.

::

	$ sudo apt-get update
	$ sudo apt-get install -y python python-pip nginx gunicorn

Create a directory to store the project.

::

	$ sudo mkdir /home/pubic_html && cd /home/public_html

Download the project from the GitHub repository and copy the application to the ``/home/public_html`` directory.

::

	$ git clone https://github.com/draperlaboratory/distill.git /home/public_html

Install Distill's requirements either globally or in a virutal environment:

::

	$ pip install -r requirements.txt

Distill has provided an nginx configuration file located in ``distill/deploy/nginx.conf``.

Gunicorn will use port 8000 and handle the incoming HTTP requests.

Restart nginx to load the configuration changes.

::

	$ sudo /etc/init.d/nginx restart

Run gunicorn on port 8000.

::

	$ gunicorn --workers 4 --bind unix:distill.sock -m 007 deploy/run_server:app 

Start a new browser instance and navigate to http://localhost.

Installing Documentation 
------------------------

To save yourself the trouble, all up to date documentation is available at https://draperlaboratory.github.io/distill/.

However, if you want to manully build the documentation, the instructions are below.

To build Distill's documentation, create a directory at the root level of ``/distill`` called distill-docs.

::

	$ mkdir distill-docs & cd distill/docs

Execute build command:

::

	# Inside top-level docs/ directory.
 	$ make html

This should build the documentation in your shell, and output HTML. At then end, it should say something about documents being ready in ``distill-docs/html``. 
You can now open them in your browser by typing

::

	$ open distill-docs/html/index.html