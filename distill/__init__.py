'''
Distill: This package contains a flask app RESTful api for distill

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from __future__ import absolute_import
import sys
from flask import Flask

if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or later is required for Distill (%d.%d detected)."
    raise ImportError (m % sys.version_info[:2])
del sys

my_app = Flask (__name__)

# Load Configurations
my_app.config.from_pyfile('config.cfg')
