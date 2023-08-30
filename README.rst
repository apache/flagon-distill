.. ..

	<!---
    Licensed to the Apache Software Foundation (ASF) under one or more
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


Apache Flagon Distill
=====================

.. image:: https://readthedocs.org/projects/incubator-flagon-distill/badge/?version=distill_toolkit_refactor
	:target: https://incubator-flagon-distill.readthedocs.io/en/distill_toolkit_refactor/?badge=stable
	:alt: Documentation Status

This project is a work in progress, prior to an official Apache Software Foundation release. Check back soon for important updates.

Please see our `readthedocs.org pages <https://incubator-flagon-distill.readthedocs.io/en/distill_toolkit_refactor/>`_ for documentation.

A contribution guide has been provided `here <http://flagon.incubator.apache.org/docs/contributing/>`_.

Installation
------------

To install and set up the Python project, Distill uses `Poetry <https://python-poetry.org/>`_, a dependency and package management tool. Poetry simplifies the management of project dependencies and virtual environments, ensuring consistent and reproducible builds.

Prerequisites
~~~~~~~~~~~~~

Before you begin, make sure you have the following prerequisites installed on your system:

- Python (>= 3.8)
- Poetry (>= 1.0)

You can install Poetry using ``pip``:

.. code-block:: bash

   pip install poetry

Installation Steps
~~~~~~~~~~~~~~~~~~

Follow these steps to set up and install the project:

1. Clone the repository:

    .. code-block:: bash

        git clone https://github.com/UMD-ARLIS/incubator-flagon-distill.git


2. Navigate to the project directory:

    .. code-block:: bash

        cd incubator-flagon-distill

3. Use Poetry to install project dependencies and create a virtual environment:

    .. code-block:: bash

        poetry install
   
   This command reads the ``pyproject.toml`` file and installs all required packages into a dedicated virtual environment.

4. Activate the virtual environment:

    .. code-block:: bash

        poetry shell
   
   You are now inside the project's virtual environment, which isolates the project's dependencies from your system-wide Python packages.

5. Run the tests:
   
   You can now run the tests to make sure everything installed properly. For example:

    .. code-block:: bash

        make test
   
   Remember that you need to activate the virtual environment (step 4) each time you work on the project.

Updating Dependencies
~~~~~~~~~~~~~~~~~~~~~

To update project dependencies, you can use the following command:

.. code-block:: bash

   poetry update

This command updates the ``pyproject.toml`` file with the latest compatible versions of the packages.

Uninstalling
~~~~~~~~~~~~

To uninstall the project and its dependencies, simply deactivate the virtual environment (if activated) by typing:

.. code-block:: bash

   exit

This will exit the virtual environment. You can then safely delete the project directory.

By following these installation steps, you can easily set up and manage the Python project using Poetry. Enjoy coding!
