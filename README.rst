mock-cloudsearch
================

A light weight implementation of Amazon's CloudSearch service for local
testing purposes.

There is not much here yet as I'm just fleshing out the web service. I'll aim
to start with the document /document/batch uploading as this is the first thing
I need to use it to check.

For more information see the sphinx documentation.

E.g.::

    # From a clean checkout set up all parts of this project (once off):
    python setup.py develop

    # To (re)build the sphinx documentation:
    python setup.py docs

    # Open the documentation in a browser on your machine:
    firefox docs/build/html/index.html


Quick start
-----------

Running all tests
~~~~~~~~~~~~~~~~~

The runtests.py is used for this and is called as follows::

    python runtests.py -sc nose.cfg

The nose.cfg configures the locations of the egg packages to test.

Run the server
~~~~~~~~~~~~~~

Run the server using the default conf.ini do::

    python setup.py runserver
