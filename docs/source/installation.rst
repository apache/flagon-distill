.. ..

	<!--- Licensed to the Apache Software Foundation (ASF) under one or more
	contributor license agreements.  See the NOTICE file distributed with
	this work for additional information regarding copyright ownership.
	The ASF licenses this file to You under the Apache License, Version 2.0
	(the "License"); you may not use this file except in compliance with
	the License.  You may obtain a copy of the License at

	  http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License. 
	--->

.. _installation:

Installation Guide
==================

Installing Apache Distill
-------------------------

The first step is to install Apache Distill. First, checkout the latest version of Apache Distill.

::

	$ git clone https://git-wip-us.apache.org/repos/asf/incubator-senssoft-distill.git

Apache Distill is a python project, so it can be installed like any other python library. Several operating systems (Mac OS X, Major Versions of Linux/BSD) have Python pre-installed, so you should just have to run

::
	
    $ easy_install distill

or

::

    $ pip install distill

Users are strongly recommended to install Apache Distill in a virtualenv. Instructions to setup an virtual environment will be explained below.

.. note ::

	When the package is installed via ``easy_install`` or ``pip`` this function will be bound to the ``distill`` executable in the Python installation's ``bin`` directory (on Windows - the ``Scripts`` directory).

Installing Apache Distill in an Virtual Environment
---------------------------------------------------

virtualenv is a tool to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that the Apache Distill project would need. 

Install virtualenv via pip:

::

	$ sudo env/bin/pip install virtualenv

Start by changing directory into the root of Apache Distill's project directory, and then use the virtualenv command-line tool to create a new environment:

::

	$ mkdir env 
	$ virtualenv env

Activate environment:

::

	$ source env/bin/activate

Install Apache Distill requirements:

::

	$ env/bin/pip -r requirements.txt

To build the source code and run all unit tests.

::

    $ env/bin/python setup.py develop test

Launch local Apache Distill server, running on localhost:8090:

::
	
	$ env/bin/dev 

Deactivate environment

:: 	

	$ deactivate

Running Apache Distill on Docker Compose
----------------------------------------

From the project directory, start up Apache Distill in the background.

:: 

	$ docker-compose up -d
	Starting elastic
	Starting logstash
	Starting kibana
	Starting distill
	$ docker-compose ps
	Name                Command               State                       Ports                      
	--------------------------------------------------------------------------------------------------
	distill    /bin/sh -c python distill/ ...   Up      0.0.0.0:8090->8090/tcp                         
	elastic    elasticsearch                    Up      0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp 
	kibana     /tmp/entrypoint.sh               Up      0.0.0.0:5601->5601/tcp                         
	logstash   logstash -f /etc/logstash/ ...   Up  

To stop services once you've finished with them:

::
	
	$ docker-compose stop

Deployment with Nginx and Gunicorn
----------------------------------

I will describe a setup with nginx as a web server on Ubuntu. A web server cannot communicate directly with a Flask application such as Apache Distill. Thus gunicorn will be used to act as a medium between the web server and Apache Distill. Gunicorn is like an application web server that will be running behind nginx, and it is WSGI compatible. It can communicate with applications that support WSGI – Flask, Django, etc.

Install requirements.

::

	$ sudo apt-get update
	$ sudo apt-get install -y python python-pip nginx gunicorn

Create a directory to store the project.

::

	$ sudo mkdir /home/pubic_html && cd /home/public_html

Download the project from the GitHub repository and copy the application to the ``/home/public_html`` directory.

::

	$ git clone https://git-wip-us.apache.org/repos/asf/incubator-senssoft-distill.git /home/public_html

Install Apache Distill's requirements either globally or in a virutal environment:

::

	$ env/bin/pip install -r requirements.txt

Apache Distill has provided an nginx configuration file located in ``distill/deploy/nginx.conf``.

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

First, install the documentation dependencies:

::

	$ env/bin/pip install -r doc_requirements.txt

To build Apache Distill's documentation, create a directory at the root level of ``/distill`` called distill-docs.

::

	$ mkdir distill-docs & cd distill-docs

Execute build command:

::

	# Inside top-level docs/ directory.
 	$ make html

This should build the documentation in your shell, and output HTML. At then end, it should say something about documents being ready in ``distill-docs/html``. 
You can now open them in your browser by typing

::

	$ open distill-docs/html/index.html