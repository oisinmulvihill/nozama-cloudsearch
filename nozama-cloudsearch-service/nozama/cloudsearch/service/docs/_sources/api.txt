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



