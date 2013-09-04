nozama-cloudsearch
------------------

.. contents::


A light weight implementation of Amazon's CloudSearch service for local testing
purposes. This is meant for use in functional / acceptance testing of service
which use cloud search.

The Nozama Service also implements its own REST API to allow you to get at the
data in a way you wouldn't normally be able to on Amazon CloudSearch.

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
    virtualenv nozama
    source nozama/bin/activate

    # Install from pypi:
    easy_install nozama-cloudsearch-service

    # OR
    pip install

    # download the development configuration:
    curl -O https://raw.github.com/oisinmulvihill/nozama-cloudsearch/master/nozama-cloudsearch-service/development.ini

    # Run the service:
    pserve development.ini

    Starting server in PID 6845.
    serving on 0.0.0.0:15808 view at http://127.0.0.1:15808

    # Success! Press Ctrl-c to exit.

MongoDB needs to be install and running on the system. The default set up will
using a database called 'nozama-cloudsearch'. See the development.ini
configuration file for more details.


Quick API Usage Example
~~~~~~~~~~~~~~~~~~~~~~~

If you have a running service you can try the following using curl from the
command line.

.. code-block:: sh

    # Assumes: serving on 0.0.0.0:15808 view at http://127.0.0.1:15808

    # A quick check of the version and that the service is running:
    curl -H "Content-Type: application/json" http://localhost:15808/ping
    {"status": "ok", "version": "1.0.3", "name": "nozama-cloudsearch-service"}

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
    {"info": {"rid": "999a84dc93c4358f683d6f3670ceed78787935f95b5e7315cc3814dd8a0b8988d0b4ed2deb03f65d", "cpu-time-ms": 0, "time-ms": 0.0015230178833007812}, "hits": {"found": 1, "hit": [{"id": "1246"}], "start": 0}, "match-expr": "(label 'bob')", "rank": "-text_relevance"}

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

