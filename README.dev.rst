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

