``fairtally`` developer documentation
=====================================

If you're looking for user documentation, go `here <README.rst>`_.


The project setup is documented in `a separate document <project_setup.rst>`_. Feel free to remove this document (and/or the link to this document) if you don't need it.



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

The test coverage report is available in `htmlcov/index.html`.
Running linters locally
-----------------------

Running the linters requires an activated virtualenv with the development tools installed.

.. code:: shell

    # linter
    prospector

    # recursively check import style for the fairtally module only
    isort --recursive --check-only fairtally

    # recursively check import style for the fairtally module only and show
    # any proposed changes as a diff
    isort --recursive --check-only --diff fairtally

    # recursively fix import style for the fairtally module only
    isort --recursive fairtally


You can enable automatic linting with ``prospector`` and ``isort`` on commit like so:

.. code:: shell

    git config --local core.hooksPath .githooks

Versioning
----------

Bumping the version across all files is done with bump2version, e.g.

.. code:: shell

    bump2version minor


Example report
--------------

The `example HTML report <https://fair-software.github.io/fairtally/_static/fairtally_example.html>`_ and its `screenshot <https://github.com/fair-software/fairtally/raw/main/docs/_static/fairtally_example.png>`_ need to be updated when the User Interface or example command changes.

Update example HTML report by running

.. code:: shell

  fairtally -o docs/_static/fairtally_example.html https://github.com/fair-software/fairtally https://github.com/fair-software/howfairis

Update screenshot (``docs/_static/fairtally_example.png``), for example by running Google Chrome screenshot command with:

.. code:: shell

  google-chrome --headless --disable-gpu --window-size=1150,280 --screenshot=docs/_static/fairtally_example.png docs/_static/fairtally_example.html

If size of report changed then adjust the ``--window-size`` argument value accordingly.

Making a release
----------------

Preparation
^^^^^^^^^^^

1. Update the ``CHANGELOG.md``
2. Verify that the information in ``CITATION.cff`` is correct, and that ``.zenodo.json`` contains equivalent data
3. Make sure the version has been updated.
4. Run the unit tests with ``pytest``
5. Make sure `example report <#example-report>`_ is up to date

PyPI
^^^^

In a new terminal, without an activated virtual environment or a venv3 directory:

.. code:: shell

    # prepare a new directory
    cd $(mktemp -d --tmpdir fairtally.XXXXXX)

    # fresh git clone ensures the release has the state of origin/main branch
    git clone https://github.com/fair-software/fairtally.git .

    # prepare a clean virtual environment and activate it
    python3 -m venv venv3
    source venv3/bin/activate

    # make sure to have a recent version of pip
    pip install --upgrade pip

    # install runtime dependencies and publishing dependencies
    pip install --no-cache-dir .
    pip install --no-cache-dir .[publishing]

    # clean up any previously generated artefacts
    rm -rf fairtally.egg-info
    rm -rf dist

    # create the source distribution and the wheel
    python setup.py sdist bdist_wheel

    # upload to test pypi instance (requires credentials)
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

In a new terminal, without an activated virtual environment or a venv3 directory:

.. code:: shell

    cd $(mktemp -d --tmpdir fairtally-test.XXXXXX)

    # check you don't have an existing fairtally
    which fairtally
    python3 -m pip uninstall fairtally

    # install in user space from test pypi instance:
    python3 -m pip -v install --user --no-cache-dir \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple fairtally

Check that the package works as it should when installed from pypitest.

Then upload to pypi.org with:

.. code:: shell

    # Back to the first terminal,
    # FINAL STEP: upload to PyPI (requires credentials)
    twine upload dist/*

GitHub
^^^^^^

Don't forget to also `make a release on GitHub <https://github.com/fair-software/fairtally/releases/new>`_.

DockerHub
^^^^^^^^^

To build the image, run:

.. code:: shell

    docker build -t fairsoftware/fairtally:latest .

.. code:: shell

    VERSION=<your-version>
    docker tag fairsoftware/fairtally:latest fairsoftware/fairtally:${VERSION}

Check that you have the tags you want with:

.. code:: shell

    docker images

To push the image to DockerHub, run:

.. code:: shell

    # (requires credentials)
    docker login
    docker push fairsoftware/fairtally:${VERSION}
    docker push fairsoftware/fairtally:latest

The new image and its tags should now be listed here https://hub.docker.com/r/fairsoftware/fairtally/tags?page=1&ordering=last_updated.
