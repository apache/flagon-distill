========================
Unit Testing with Pytest
========================
The distill package uses ``pytest`` as a means to validate our functions.  Below we describe how to run these tests:

Running Unit Tests
------------------
Unit tests can be run through the command line, provided that ``pytest`` is installed on your machine.  If ``pytest`` is not installed, it can be installed with the following command:
::
    pip install pytest
Once ``pytest`` is installed, you can navigate to the tests directory and begin running unit tests using the following commands:
::
    cd tests
    export PYTHONPATH=../
    pytest
Note that we must set the PYTHONPATH environment variable to the top level distill directory (or ../ in this case).  This ensures that ``pytest`` knows where to look for the distill package.

Common Issues
*************
The most common issues when running the unit tests with ``pytest`` are that the PYTHONPATH is set incorrectly (or not set at all) or that modules needed to run the tests are not installed on your machine.

To solve these issues, make sure that the PYTHONPATH is set to the proper directory prior to running ``pytest`` and install any modules that ``pytest`` describes as missing (the missing modules should be explained in the error messages).

Test Coverage
-------------
``Pytest`` can also be used to determine test coverage statistics.  This can be done by installing the ``pytest-cov`` plugin.
::
    pip install pytest-cov

Once this is installed, coverage statistics on the distill package can be obtained through the following commands:
::
    cd tests
    export PYTHONPATH=../
    pytest --cov=distill ./