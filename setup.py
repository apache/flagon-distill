'''
Distill: An analytical framework for User-ALE <https://github.com/draperlaboratory/user-ale>.

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

You can install Distill with "python setup.py install"

Copyright 2016, The Charles Stark Draper Laboratory, Inc.
Licensed under Apache Software License
'''

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io, os, sys

here = os.path.abspath(os.path.dirname (__file__) )

if sys.argv[-1] == 'setup.py':
    print ("To install, run 'python setup.py install'")
    print ()
    
def read (*filenames, **kwargs):
    encoding = kwargs.get ('encoding', 'utf-8')
    sep = kwargs.get ('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open (filename, encoding=encoding) as f:
            buf.append (f.read ())
    return sep.join (buf)

# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest (TestCommand):
    def finalize_options (self):
        TestCommand.finalize_options (self)
        self.test_args = []
        self.test_suite = True

    def run_tests (self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit (pytest.main (self.test_args))

setup (
    name = "Distill",
    version = "1.0",
    url = "https://github.com/draperlaboratory/distill",
    license = "Apache Software License",
    author = "Michelle Beard",
    author_email = "mbeard@draper.com",
    description = "An analytical framework for User-ALE.",
    long_description = __doc__,
    classifiers = [
      'Development Status :: 4 - Beta',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Natural Language :: English',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: OS Independent', 
      'Private :: Do Not Upload"'
    ],
    keywords = "analytics graph stout user-ale instrumentation", # Separate with spaces
    packages = find_packages (exclude=['examples', 'tests']),
    include_package_data = True,
    zip_safe = False,
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
    install_requires = ['Flask==0.10.1', 
                        'networkx==1.11',
                        'elasticsearch-dsl==2.0.0', 
                        'numpy>=1.10.0', 
                        'scipy>=0.17.0',
                        'sphinx>=1.4.0'
    ],
    entry_points = {
      'console_scripts': [
        'dev = distill.deploy.run_server:dev_server'
        ]
    }
)
