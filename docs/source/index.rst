Welcome to nozama-cloudsearch documentation!
=============================================

Contents:

.. toctree::
   :maxdepth: 3

   api.rst
   developer.rst


Introduction
------------

The aim of this project is to emulate the Amazon CloudSearch interface for
local testing purposes. I don't intend this project to be used as a replacement
for cloud search.

I wanted to test a platfom that was hardcoded to use only cloudsearch. There
was no way I could change the code in question. I was also unable to get other
instances due to budget constraints. I looked around for alternatives and found
none I could get working on CentOS.

One handy benefit of using Nozama is it provides a way to migrate from Amazon
CloudSearch to ElasticSearch.


Releases
--------

1.1.3
~~~~~

This is a minor fix to the LICENSE file as spotted by Alex (https://github.com/ALyman).

 * https://github.com/oisinmulvihill/nozama-cloudsearch/issues/1

1.1.2
~~~~~

Evasion common is a dependancy add wasn't being listed, which it now is.

1.1.1
~~~~~

A minor fix to specify requests 1.2.3 as the version to be used. This allowed
pyelastic search to work along with nozama and evasion common.

1.1.0
~~~~~

ElasticSearch is now used to index the document fields which have been batch
uploaded. The system still uses MongoDB to record what was uploaded and
removed. The search currently does a text search via the q parameter. Facets
are not yet supported.

 * http://www.elasticsearch.org/

I maybe look at removing MongoDB and use ElasticSearch exclusively. For the
moment this is good enough for me.


1.0.6
~~~~~

This implements the batch upload and provides the search api. The search is
not filtering. It will return all documents stored. MongoDB is used to store
uploaded and removed documents.

The API /dev/documents allows up to inspect the results of a batch upload. This
aids testing applications which create the batch upload.


Alternative projects
~~~~~~~~~~~~~~~~~~~~~

I came across Groonga CloudSearch which implements a local instance of Amazon
CloudSearch. I tried hard to get it to work on CentOS and Ubuntu. Sadly it
didn't work for me. Its NodeJS codebase needs updating. Something I don't have
the time to learn and try.

It may be worth keeping and eye on incase it comes to life again.

 * http://gcs.groonga.org/docs/


Documentation
-------------

 * http://nozama-cloudsearch.readthedocs.org/en/latest


Source Code
-----------

 * https://github.com/oisinmulvihill/nozama-cloudsearch



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`