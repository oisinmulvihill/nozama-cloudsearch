# -*- coding: utf-8 -*-
"""
"""
import os
import json
import logging

import requests

from nozama.cloudsearch.data.db import db
from nozama.cloudsearch.data.db import get_es
#from nozama.cloudsearch.data.db import ElasticSearchHelper


def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


def all():
    """Return all the stored documents.
    """
    log = get_log('all')
    conn = db().conn()

    returned = list(conn.documents.find())
    log.debug("Returning '{0}' documents".format(len(returned)))

    return returned


def removed():
    """Return all the documents which have been removed.
    """
    log = get_log('removed')
    conn = db().conn()

    returned = list(conn.documents_removed.find())
    log.debug("Returning '{0}' documents".format(len(returned)))

    return returned


import formencode
from formencode import validators


class FieldsSchema(formencode.Schema):
    """The data to be searched. I think anything goes here.
    """
    allow_extra_fields = True


class DocSchema(formencode.Schema):
    """Validate the document and the add/remove operation.

    """
    allow_extra_fields = True

    id = validators.String(not_empty=True, strip=True)

    lang = validators.String(not_empty=True, strip=True, if_missing='en')

    #fields = FieldsSchema(not_empty=True)

    version = validators.String(not_empty=True, strip=True)

    type = validators.OneOf(
        ["add", "delete"], not_empty=True, strip=True,
    )


DOC_SCHEMA = DocSchema()


HEADERS = {"Content-Type": "application/json"}


def add_to_elasticsearch(doc):
    """
    """
    log = get_log('add_to_elasticsearch')
    es = get_es()

    log.debug("adding doc <{0}>".format(doc['id']))

    # result = es.conn.put(
    #     '{0}/{1}'.format(es.document_path, doc['id']),
    #     data=doc['fields']
    # )
    data = json.dumps(doc['fields'])
    response = requests.post(es.document_uri, data=data, headers=HEADERS)
    result = response.json

    log.debug("doc <{0}> add result: {1}".format(doc['id'], result))


def search(query={}):
    """Perform a search across text fields.

    :returns: A dict compatible with an Amazon CloudSearch response.

    """
    log = get_log('search')
    es = get_es()

    qstring = query.get('q', '')
    log.debug("searching query '{0}'".format(query))

    # import pdb ; pdb.set_trace()
    if qstring:
        data = '{"query": {"query_string": {"query": "%s"}}}' % qstring
        data = json.dumps(data)
        response = requests.get(es.search_uri, data=data, headers=HEADERS)

    else:
        response = requests.get(es.search_uri, headers=HEADERS)

    import pdb ; pdb.set_trace()

    results = response.json

    request_id = os.urandom(40).encode('hex')

    rc = {
        "rank": "-text_relevance",
        "match-expr": "(label '{0}')".format(qstring),
        "hits": {
            "found": results['hits']['total'],
            "start": 0,
            "hit": [i['_id'] for i in results['hits']['hits']]
        },
        "info": {
            "rid": request_id,
            "time-ms": results['took'],
            "cpu-time-ms": 0
        }
    }

    log.debug("found '{0}'".format(rc))

    return rc


def load(docs_to_load):
    """Load documents in the Amazon SDF an add/remove from mongo accordingly.

    Each document will be validated against DocSchema.

    :returns: An amazon compatible documents/batch Response Property dict.

    For example:

    .. code-block:: python

        rc = dict(
            status='ok',
            adds=len(to_load),
            deletes=len(to_remove),
            error='',
            warning='',
        )

    Reference:
      * http://docs.aws.amazon.com/cloudsearch/latest/developerguide/\
            DocumentsBatch.JSON.html#DocumentsBatch.JSON.ResponseProperties

    """
    log = get_log('load')
    conn = db().conn()

    to_load = []
    to_remove = []

    # Validate the data first then bulk add/remove if all goes well.
    for doc in docs_to_load:
        # validate against what amazon would expect from the SDF.
        doc = DOC_SCHEMA.to_python(doc)
        if doc['type'] == "add":
            # used the doc's id as the unique id for the mongodb document.
            doc['_id'] = doc['id']
            # not need in storage:
            doc.pop('type')
            log.debug("to_load: {0}".format(doc))
            to_load.append(doc)

        else:
            # remove
            log.debug("to remove: '{0}'".format(doc))
            to_remove.append(doc)

    if to_load:
        log.debug("bulk loading: '{0}' document(s)".format(len(to_load)))
        conn.documents.insert(to_load)
        for doc in to_load:
            add_to_elasticsearch(doc)

    if to_remove:
        doc_ids = [doc['id'] for doc in to_remove]

        # Recover the documents that have been removed in this upload and
        # store it on the removed list.
        for doc_id in doc_ids:
            query = dict(_id=doc_id)
            found = conn.documents.find_one(query)
            if found:
                log.debug("adding to remove store: '{0}'".format(query))
                conn.documents_removed.insert(found)
                conn.documents.remove(query)

    rc = dict(
        status='ok',
        adds=len(to_load),
        deletes=len(to_remove),
        error='',
        warning='',
    )

    return rc


def configure_field(domain, name, field_type):
    """Set up the full text indexing and how the type information is handled.

    :param domain: Not used for now, possibly with be to collection or db.

    :param name: The field inside the batch upload to set the index for.

    :param field_type: The type information. Only 'text' is implemented.

    I'm going to make it compatible with how Amazon does it. Although for now
    I'm just going to get FTI working using what MongoDB provides.

    """
    log = get_log('configure_field')

    #conn = db().conn()
    field_type = field_type.strip().lower()

    log.debug("domain <{0}> name<{1}> field_type<{2}>".format(
        domain, name, field_type
    ))


def report():
    """Return a list of a documents added and removed by batch uploading.

    :returns: a dict.

    E.g.:

        {
            "documents": [
                # A list of documents currently stored from all batch upload
                # so far.
                :
            ],
            "documents_removed": [
                # A list of documents that have been removed from all batch
                # uploads so far.
                :
            ]
        }

    """
    return {"documents": all(), "documents_removed": removed()}


def remove_all():
    """Remove all store documents.
    """
    log = get_log('remove_all')
    conn = db().conn()
    conn.documents.drop()
    conn.documents_removed.drop()
    log.warn("all documents have been removed.")
