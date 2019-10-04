# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

##TODO Update for WIP-PACKAGE

import setuptools
import io
import os
import sys

if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or later is required for Distill (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'\n")
    print("To run tests, run 'python setup.py test'\n")
    print("To build docs, run 'python setup.py docs'\n")
    print("To clean, run 'python setup.py clean'\n")


class CleanCommand(setuptools.Command):
    """
    A command class to clean up build artifacts, including log files

    python setup.py clean
    """
    description = "clean build artifacts"
    user_options = []

    def initialize_options(self):
        """
        Initialize Clean Command
        """
        self.cwd = None

    def finalize_options(self):
        """
        Set Current Working directory for Clean Command

        """
        self.cwd = os.getcwd()

    def run(self):
        """
        Execute Clean Command
        """
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -rf ./docs/_build ./build ./dist ./*.egg-info')
        os.system('rm -rf ./*.log *.xml .coverage *.html')

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


# Get the version string
def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'distill/version.py')) as f:
        version = {}
        exec (f.read(), version)
        return version['__version__']
    raise RuntimeError('No version info found.')


setup_requires = [
    'pip >= 9.0.1',
    'setuptools >= 34.0',
    'pytest-runner',
]

install_requires = [
    'elasticsearch-dsl >= 5.0.0, < 6.0.0',
    # 'pandas >= 0.20.2',
    'Flask >= 0.12.2',
    'celery >= 4.0.2',
]

tests_require = [
    'pytest >= 3.0.0',
    'pytest-pylint',
    'pytest-html',
    'pytest-cov',
]

docs_require = [
    'Sphinx >= 1.5.2',
    'sphinx-rtd-theme >= 0.1.9',
]

extras_require = {
    'test' : tests_require,
    'doc' : docs_require,
    'monitor': [
        'flower'
    ]
}

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Environment :: Web Environment',
    'Framework :: Flask',
    'Topic :: Internet :: Log Analysis'
]

setuptools.setup(
    name="Distill",
    version=get_version(),
    url="http://senssoft.incubator.apache.org",
    license="Apache Software License 2.0",
    author="Michelle Beard",
    author_email="mbeard@apache.org",
    description="An analytical framework for UserALE and TAP.",
    long_description=__doc__,
    classifiers=classifiers,
    keywords="stout userale tap distill",
    packages=setuptools.find_packages(exclude=['examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'clean': CleanCommand,
    },
    setup_requires=setup_requires,
    tests_require=tests_require,
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'dev = distill.server:dev_server'
        ]
    }
)
