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
API. The <api version> can be any string currently, I don't check or enforce
any value here.

Reference:
 * http://docs.aws.amazon.com/cloudsearch/latest/developerguide/SvcIntro.html


POST /<api version>/documents/batch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is used to batch load documents for later querying. This loads documents
from the Amazon SDF and adds/removes from mongo accordingly.

This will return a JSON response property:

    .. code-block:: python

        rc = dict(
            status='ok',
            adds=0+,
            deletes=0+,
            error='',
            warning='',
        )

Reference:
 * http://docs.aws.amazon.com/cloudsearch/latest/developerguide/DocumentsBatch.JSON.html#DocumentsBatch.JSON.ResponseProperties


GET /<api version>/search
~~~~~~~~~~~~~~~~~~~~~~~~~

Currently this does not filter the result or perform any search. It will return
the ids of all documents on the system. It will look at the "q" parameter and
recover the string it should be restricting. It will put this in the match-expr
returned.

I intend to implement search. For the moment I just need a response rather then
not having search at all.

This will return a JSON response:

    .. code-block:: python

        # example return
        {
            'rank': '-text_relevance'
            'match-expr': "(label 'skate board')",
            'hits': {
                'found': 1,
                'start': 0
                'hit': [
                    {'id': u'1382'}
                ],
            },
            'info': {
                'rid': '128a5a6b5881d7d28252ef835961d6538a04b99b74c420011fc081496eb36baedc17b278a6f29979',
                'cpu-time-ms': 0,
                'time-ms': 0.0010879039764404297
            },
        }

The rank is hard coded to '-text_relevance' for the moment. The hits/found is
the amount of documents on the system. The hits/hit will be a list of all
document ids currently added to the system. This will match the 'documents'
section in that JSON returned by a GET of '/dev/documents'.

The rid will be generated each time. The time-ms will also be calculated based
on the time it take to run a query. The cpu-time-ms is currently hard coded to
0.


Reference:
 * http://docs.aws.amazon.com/cloudsearch/latest/developerguide/searching.html


Nozama Specific
---------------


GET /dev/documents
~~~~~~~~~~~~~~~~~~

This will return all documents add and removed from the the system by
subsequent batch uploads.

.. code-block:: python

    # This returns a list of ...

    {
        'documents_removed': [
            {
                'lang': 'en',
                'fields': {...},
                'version': '...',
                'id': '...'
            },
            :
            etc
        ],
        'documents': [
            {
                'lang': 'en',
                'fields': {...},
                'version': '...',
                'id': '...'
            },
            :
            etc
        ]
    }


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
        # This will contain the current version number.
        'version': 'X.Y.Z',
        'name': 'nozama-cloudsearch-service'
    }


GET /docs/
~~~~~~~~~~

The service self hosts its own documentation. This is the same
