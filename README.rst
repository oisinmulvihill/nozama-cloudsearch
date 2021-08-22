nozama-cloudsearch
------------------

.. contents::

A light weight implementation of Amazon's CloudSearch service for local testing
purposes. This is meant for use in functional / acceptance testing of service
which use cloud search.

The Nozama Service also implements its own REST API to allow you to get at the
data in a way you wouldn't normally be able to on Amazon CloudSearch.

One handy benefit of using Nozama is it provides a way to migrate from Amazon
CloudSearch to ElasticSearch.

The "official" docker container:

 - https://hub.docker.com/r/oisinmulvihill/nozama-cloudsearch

The Github repository:

  - https://github.com/oisinmulvihill/nozama-cloudsearch

Why?
----

I wanted to test a platform that was hardcoded to use only Cloudsearch. There
was no way I could change the code in question. I was also unable to get other
instances due to budget constraints. I looked around for alternatives and found
none I could get working on CentOS.


Quick-start
-----------

Docker
~~~~~~

If you have docker and docker-compose on your system already then you can do:

.. code-block:: sh

    # download the docker compose configuration:
    curl -O https://raw.githubusercontent.com/oisinmulvihill/nozama-cloudsearch/master/nozama-cloudsearch.yaml

    # Run in the background:
    docker-compose -f nozama-cloudsearch.yaml up -d

    # Check everything is up and running
    docker-compose -f nozama-cloudsearch.yaml ps

    curl http://localhost:15808/ping
    {"status": "ok", "name": "nozama-cloudsearch", "version": "2.0.3"}

    # To shutdown and stop all parts:
    docker-compose -f nozama-cloudsearch.yaml down

This will download the Mongo and ElasticSearch containers which it depends on. Once all services have been downloaded you can then start using the REST API.

Pypi.org
~~~~~~~~

Mongo and ElasticSearch need to be installed and running on the system. The default set up will use a database called 'nozama-cloudsearch'. See the development.ini configuration file for more details.

.. code-block:: sh

  # create a quick environment to install into:
  mkvirtualenv -p python 3 nozama

  # activate en
  workon nozama

  # Install from pypi:
  pip install nozama-cloudsearch

  # download the development configuration:
  curl -O https://raw.githubusercontent.com/oisinmulvihill/nozama-cloudsearch/master/development.ini

  # Run the service:
  pserve development.ini

  Starting server in PID 6845.
  serving on 0.0.0.0:15808 view at http://127.0.0.1:15808

Success!


Quick API Usage Example
-----------------------

If you have a running service you can try the following using curl from the
command line.

.. code-block:: sh

    # Assumes: serving on 0.0.0.0:15808 view at http://127.0.0.1:15808

    # A quick check of the version and that the service is running:
    curl http://localhost:15808/ping
    {"status": "ok", "name": "nozama-cloudsearch", "version": "2.0.3"}

    # Now check what documents are present / removed:
    curl http://localhost:15808/dev/documents
    {"documents_removed": [], "documents": []}

    # Add a document using the batch upload SDF:
    curl -X POST -H "Content-Type: application/json" http://localhost:15808/2013-08-22/documents/batch -d '[{"lang": "en", "fields": {"name": "bob"}, "version": 1376497963, "type": "add", "id": 1246}]'
    {"status": "ok", "adds": 1, "deletes": 0, "error": "", "warning": ""}

    # Check the document is there:
    curl http://localhost:15808/dev/documents
    {"documents": [{"_id": "1246", "lang": "en", "fields": {"name": "bob"}, "version": "1376497963", "id": "1246"}], "documents_removed": []}

    # Try searching for the document:
    curl http://localhost:15808/2013-08-22/search?q=bob
    {"rank": "-text_relevance", "match-expr": "(label 'bob')", "hits": {"found": 1, "start": 0, "hit": [{"id": "1246", "fields": {"name": "bob"}}]}, "info": {"rid": "47e87151546d5a349d7bf9b60eee0ebdf74783422a2e08cad0b9348e3ee3ef04eb198715bbe4e353", "time-ms": 5, "cpu-time-ms": 0}}

    curl http://localhost:15808/2013-08-22/search?q=somethingnotpresent
    {"rank": "-text_relevance", "match-expr": "(label 'somethingnotpresent')", "hits": {"found": 0, "start": 0, "hit": []}, "info": {"rid": "869d2b07c1e47a55ab1cb4cd615953333e52d886112e916ed7fa447355f5a518b1c16bbcbf40cb7e", "time-ms": 5, "cpu-time-ms": 0}}

    # Remove the document in another batch update:
    curl -X POST -H "Content-Type: application/json" http://localhost:15808/2013-08-22/documents/batch -d '[{"version": 1376497963, "type": "delete", "id": 1246}]'
    {"status": "ok", "adds": 0, "deletes": 1, "error": "", "warning": ""}

    # Check what was removed:
    curl http://localhost:15808/dev/documents
    {"documents": [], "documents_removed": [{"_id": "1246", "lang": "en", "fields": {"name": "bob"}, "version": "1376497963", "id": "1246"}]}

    # Empty out all stored content:
    curl -X DELETE http://localhost:15808/dev/documents
    {"status": "ok", "message": "Documents Removed OK.", "error": "", "traceback": ""}

    # Check there should now be nothing there:
    curl http://localhost:15808/dev/documents
    {"documents": [], "documents_removed": []}


Development
-----------

I develop and maintain project on Mac OSX. I have install docker-composer, docker, virtualenvwrappers and Python3 using brew. I use "make" to aid development.

.. code-block:: sh

    # create a quick environment to install into:
    mkvirtualenv --clear -p python3 nozama

    # (activate if needed)
    workon nozama

    # Install the project dependancies
    make install

    # Start the project dependancies ElasticSearch and Mongo
    make up

    # Run the API locally:
    make run


Contributing
------------

Submit a pull request with tests if possible. I'll review, test and usually approve. All tests must pass. I run against Python3 nowadays. I will then increment the version, add attribute and then release to https://hub.docker.com/r/oisinmulvihill/nozama-elasticsearch and pypi.org if all is good.

Release Process
---------------

Help Oisin remember the release process:

.. code-block:: sh

    # clean env for release:
    mkvirtualenv --clear -p python3.7 nozama

    # setup and run all tests:
    #
    # make sure mongo and elasticsearch are running:
    make up

    # run all unit and acceptance tests in a completely isolated environment.
    make docker_test

    # Build and release to test.pypi.org first:
    make test_pypi_release

    # If all is good time to release to pypi.org
    make release_to_pypi

    # Now release the new docker container
    make docker_release

Try pip install and docker pull for the new package and container.

Versions
--------

2.0.4
~~~~~

Bug fix contributed by https://github.com/lilsweetcaligula for issue https://github.com/oisinmulvihill/nozama-cloudsearch/issues/15.

2.0.3
~~~~~

Bugfix to add in __init__.py files. I had forgotten to do this after I ditched the namespace packaging.

2.0.3
~~~~~

Stripped out the old sphinx docs from the API. http://localhost:15808/docs/ now just shows a link to Github REST API examples. Strip out unused code in the client side code and other unused files.

2.0.0 -> 2.0.1
~~~~~~~~~~~~~~

Updated the project after noticing lots of people still appear to use it. I've updated it to reflect my current thinking on building REST APIs and how they are packaged, developed and released.

Changes:

- REST API remains the same however searching now works.
- Migrated to Python 3.
- Refactor the project into a single python package making it easier to work on and contribute to.
- Development is now assisted using docker compose to manage Mongo and ElasticSearch dependancies.
- I now produce the "offical" nozama-cloudsearch container as part of my release process.
- Unpinned the python dependancies and moved to using requirements files for production and testing requirements.

1.2.0
~~~~~
Add support for multibyte characters.

 * https://github.com/oisinmulvihill/nozama-cloudsearch/pull/9

Return field values and support `sdk` format.

 * https://github.com/oisinmulvihill/nozama-cloudsearch/pull/8

Remove unnecessary validations.

 * https://github.com/oisinmulvihill/nozama-cloudsearch/pull/7

Upsert a document.

 * https://github.com/oisinmulvihill/nozama-cloudsearch/pull/6

Contributed by hokuma(https://github.com/hokuma)

1.1.3
~~~~~

This is a minor fix to the LICENSE file as spotted by Alex (https://github.com/ALyman).

 * https://github.com/oisinmulvihill/nozama-cloudsearch/issues/1
