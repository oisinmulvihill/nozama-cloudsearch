Developer Guide to Project
==========================

Contents:

.. toctree::
   :maxdepth: 3


Quick start
-----------

The nozama-cloudsearch REST service repository checkout contains multiple parts
that get built into eggs. Paver is used to make it appear as one "egg" from the
top level. This mean setup.py develop | bdist_egg and other commands can be
used. All contained parts will then have the command run on them.

For example, to set up all contained eggs in development mode::

    python setup.py develop


Run the server
~~~~~~~~~~~~~~

Run the server using the default "development.ini" do::

    python setup.py runserver

Behind the scenes this will changed into the Service directory. It will then
run "pserver --reload development.ini". The default port for the service is
"63833" and you can go to "http://localhost:63833" in your
browser and see the top level status page.


Project Parts
-------------

docs
~~~~

The project containing the sphinx documentation for all contained project
parts. The documentation can be built using paver from the top level of the
project.

From a development checkout you can do the following::

    $python setup.py  docs
    ---> pavement.docs
    make html
    sphinx-build -b html -d build/doctrees   source build/html
    Running Sphinx v1.1.3
    loading pickled environment... done
    building [html]: targets for 1 source files that are out of date
    updating environment: 0 added, 1 changed, 0 removed
    reading sources... [100%] index
    :
    etc
    :
    Build finished. The HTML pages are in build/html.

    You can now open the index.html in your browser:

        docs/build/html/index.html

    $

You can then run the command to open the newly built docs in Firefox::

    firefox docs/build/html/index.html


Data
~~~~

This part provides the business logic and core code behind the cloudsearch
project. This delivers the namespace "nozama.cloudsearch.data" into the
environment. The Service builds on this to provide the REST API.


Service
~~~~~~~

This part provides the Pyramid REST Service egg. This delivers the namespace
"nozama.cloudsearch.service" into the environment. You can run the development
version of the service using paver, as stated in the quick start, or from the
Service directory directly.

For example::

    cd nozama-cloudsearch-service
    pserve --reload development.ini


Client
~~~~~~

This part provides the python client library the consumes the REST API,
provided by the Service. This delivers the namespace "nozama.cloudsearch.client"
into the environment.

A quick test of the client library against a running service is::

    from nozama.cloudsearch.client.rest import CloudsearchService

    # If the URL of the service is not provide localhost:63833 is used
    # by default.
    #
    api = CloudsearchService("http://localhost:63833")

    api.ping()
    >>> {u'status': u'ok', u'version': u'1.0.0dev', u'name': u'nozama-cloudsearch-service'}

    # Success!


Tools
-----

cloudsearch-admin
~~~~~~~~~~~~~~~~~

The Client egg also sets up the cloudsearch-admin command line admin tool. This
is used to perform various adminstration activities on a running Service. It
consumes the REST client library to perform its actions.



