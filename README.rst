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

The running Nozama Service hosts its own docs generated from sphinx. I've also
upload to readthedocs.org here:

* https://nozama-cloudsearch.readthedocs.org/en/latest/index.html

Locally hosted docs:

* http://localhost:15808/docs/index.html


Why?
~~~~

I wanted to test a platfom that was hardcoded to use only cloudsearch. There
was no way I could change the code in question. I was also unable to get other
instances due to budget constraints. I looked around for alternatives and found
none I could get working on CentOS.


Quickstart
----------

To get up and going on a system with MongoDB running do:

.. code-block:: sh

    # create a quick environment to install into:
    mkvirtualenv -p python 3 nozama

    # activate en
    workon nozama

    # Install from pypi:
    easy_install nozama-cloudsearch

    # OR
    pip install

    # download the development configuration:
    curl -O https://raw.github.com/oisinmulvihill/nozama-cloudsearch/master/nozama-cloudsearch/development.ini

    # Run the service:
    pserve development.ini

    Starting server in PID 6845.
    serving on 0.0.0.0:15808 view at http://127.0.0.1:15808

    # Success! Press Ctrl-c to exit.

MongoDB needs to be install and running on the system. The default set up will
use a database called 'nozama-cloudsearch'. See the development.ini
configuration file for more details.

Quick API Usage Example
~~~~~~~~~~~~~~~~~~~~~~~

If you have a running service you can try the following using curl from the
command line.

.. code-block:: sh

    # Assumes: serving on 0.0.0.0:15808 view at http://127.0.0.1:15808

    # A quick check of the version and that the service is running:
    curl -H "Content-Type: application/json" http://localhost:15808/ping
    {"status": "ok", "version": "1.1.0", "name": "nozama-cloudsearch"}

    # Now check what documents are present / removed:
    curl -H "Content-Type: application/json" http://localhost:15808/dev/documents
    {"documents_removed": [], "documents": []}

    # Add a document using the batch upload SDF:
    curl -X POST -H "Content-Type: application/json" http://localhost:15808/2013-08-22/documents/batch -d '[{"lang": "en", "fields": {"name": "bob"}, "version": 1376497963, "type": "add", "id": 1246}]'
    {"status": "ok", "warning": "", "adds": 1, "error": "", "deletes": 0}

    # Check the document is there:
    curl -H "Content-Type: application/json" http://localhost:15808/dev/documents
    {"documents_removed": [], "documents": [{"lang": "en", "fields": {"name": "bob"}, "_id": "1246", "version": "1376497963", "id": "1246"}]}

    # Try searching for the document:
    curl -H "Content-Type: application/json" http://localhost:15808/2013-08-22/search?q=bob
    {"info": {"rid": "5ac832321dd35dfe1f3151689ab019bac24f5e2acf4d5f9f46516329988c3967109f3ae0ba59b345", "cpu-time-ms": 0, "time-ms": 2}, "hits": {"found": 1, "hit": [{"id": "1246"}], "start": 0}, "match-expr": "(label 'bob')", "rank": "-text_relevance"}

    curl -H "Content-Type: application/json" http://localhost:15808/2013-08-22/search?q=somethingnotpresent
    {"info": {"rid": "71b70eba393d9f79858a1e09d1cf8e1a337c4d3f954631babdc6de891e202d5416ff699e85fa76ba", "cpu-time-ms": 0, "time-ms": 0}, "hits": {"found": 0, "hit": [], "start": 0}, "match-expr": "(label 'somethingnotpresent')", "rank": "-text_relevance"}

    # Remove the document in another batch update:
    curl -X POST -H "Content-Type: application/json" http://localhost:15808/2013-08-22/documents/batch -d '[{"version": 1376497963, "type": "delete", "id": 1246}]'
    {"status": "ok", "warning": "", "adds": 0, "error": "", "deletes": 1}

    # Check what was removed:
    curl -H "Content-Type: application/json" http://localhost:15808/dev/documents
    {"documents_removed": [{"lang": "en", "fields": {"name": "bob"}, "_id": "1246", "version": "1376497963", "id": "1246"}], "documents": []}

    # Empty out all stored content:
    curl -X DELETE -H "Content-Type: application/json" http://localhost:15808/dev/documents
    {"status": "ok", "message": "Documents Removed OK.", "traceback": "", "error": ""}

    # Check there should now be nothing there:
    curl -H "Content-Type: application/json" http://localhost:15808/dev/documents
    {"documents_removed": [], "documents": []}


Development
-----------

I develop and maintain project on Mac OSX. I have install docker-composer, docker and python3 using brew. I use make to aid development and release. I've migrated the project from Python2 over to Python 3.

.. code-block:: sh

    # create a quick environment to install into:
    mkvirtualenv --clear -p python3 nozama

    # (activate if needed)
    workon nozama

    # Install the project dependancies
    make install

    # Start the project dependancies ElasticSearch and Mongo
    make up




Versions
--------

2.0.0
~~~~~

Migrated to Python 3 and refactored code into a single project. I've unpinned the project dependancies and all tests pass.

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
