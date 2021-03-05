``fairtally`` developer documentation
=====================================

If you're looking for user documentation, go `here <README.rst>`_.

|
|

Development install
-------------------

.. code:: shell

    # Create a virtualenv, e.g. with
    python3 -m venv venv3

    # activate virtualenv
    source venv3/bin/activate

    # make sure to have a recent version of pip
    pip install --upgrade pip

    # (from the project root directory)
    # install fairtally as an editable package
    pip install --no-cache-dir --editable .
    # install development dependencies
    pip install --no-cache-dir --editable .[dev]

Afterwards check that the install directory was added to the ``PATH``
environment variable. You should then be able to call the executable,
like so:

.. code:: shell

    fairtally --help


Running the tests
-----------------

Running the tests requires an activated virtualenv with the development tools installed.

.. code:: shell

    # unit tests with mocked representations of repository behavior
    pytest
    pytest tests/


Running linters locally
-----------------------

Running the linters requires an activated virtualenv with the development tools installed.

.. code:: shell

    # linter
    prospector

    # recursively check import style for the howfairis module only
    isort --recursive --check-only fairtally

    # recursively check import style for the fairtally module only and show
    # any proposed changes as a diff
    isort --recursive --check-only --diff fairtally

    # recursively fix  import style for the howfairis module only
    isort --recursive fairtally

.. code:: shell

    # requires activated virtualenv with development tools
    prospector && isort --recursive --check-only fairtally

You can enable automatic linting with ``prospector`` and ``isort`` on commit like so:

.. code:: shell

    git config --local core.hooksPath .githooks

