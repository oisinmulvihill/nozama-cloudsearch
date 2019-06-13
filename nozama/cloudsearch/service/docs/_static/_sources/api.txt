REST API For Nozama CloudSearch
===============================

Contents:

.. toctree::
   :maxdepth: 3


Introduction
------------

This documents the CloudSearch API I am implementing and how its called. I
also document the Nozama specifc REST API used to check the outcomes of earlier
calls.


Amazon CloudSearch
------------------

These are the REST API calls I currently implement from Amazon's CloudSearch
API.

Reference:
 * http://docs.aws.amazon.com/cloudsearch/latest/developerguide/SvcIntro.html


POST /<api version>/documents/batch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is used to batch load documents for later querying.

Reference:
 * http://docs.aws.amazon.com/cloudsearch/latest/developerguide/DocumentsBatch.JSON.html#DocumentsBatch.JSON.ResponseProperties


Nozama Specific
---------------


GET /dev/documents
~~~~~~~~~~~~~~~~~~

This will return all documents currently stored on the system. This is useful
for seeing the results of a batch upload.

.. code-block:: python

    # This returns a list of ...


DELETE /dev/documents
~~~~~~~~~~~~~~~~~~~~~

This will remove all documents currently stored on the system. This is useful
for cleaning out before a test run.

.. code-block:: python

    # This returns a status dict e.g.:
    {
        'status': 'ok',
        'message': 'Documents Removed OK.',
        'traceback': '',
        'error': ''
    }


GET /ping
~~~~~~~~~

This can be used to check the service is up and running. It will return a JSON
structure in the form:

.. code-block:: python

    {
        'status': 'ok',
        'version': 'X.Y.Z',
        'name': 'nozama-cloudsearch-service'
    }
