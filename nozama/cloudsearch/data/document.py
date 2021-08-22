# -*- coding: utf-8 -*-
"""
"""
import os
import logging
import binascii
from datetime import datetime

import formencode
from formencode import validators

from nozama.cloudsearch.data.db import db
from nozama.cloudsearch.data.db import get_es


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

    version = validators.String(
        strip=True, if_missing=datetime.now().strftime('%s')
    )

    type = validators.OneOf(
        ["add", "delete"], not_empty=True, strip=True,
    )


DOC_SCHEMA = DocSchema()


HEADERS = {"Content-Type": "application/json"}


def add_to_elasticsearch(doc):
    """This indexes the fields and puts them into cloud search for later
    searching.

    """
    log = get_log('add_to_elasticsearch')
    es = get_es()

    log.debug("adding doc <{0}>".format(doc['id']))

    result = es.conn.create(
        index=es.index,
        id=doc['_id'],
        body=doc['fields'],
    )
    es.conn.indices.refresh(index=es.index)

    log.debug("doc <{0}> add result: {1}".format(doc['id'], result))


def remove_from_elasticsearch(doc):
    """Remove this document from the index.

    """
    log = get_log('remove_from_elasticsearch')
    es = get_es()

    log.debug("remove doc <{0}>".format(doc['id']))

    result = es.conn.delete(
        es.index,
        doc['id']
    )
    es.conn.indices.refresh(index=es.index)

    log.debug("doc <{0}> remove result: {1}".format(doc['id'], result))


def search(query={}):
    """Perform a search across text fields.

    :returns: A dict compatible with an Amazon CloudSearch response.

    """
    log = get_log('search')
    es = get_es()

    qstring = query.get('q', '')
    log.debug("searching query '{0}'".format(query))
    formatType = query.get('format', '')

    # try:
    if qstring:
        query = {
            "query": {
                "query_string": {
                    "query": u"{0}*".format(qstring)
                }
            }
        }
        results = es.conn.search(index=es.index, body=query)

    else:
        query = {"query": {"match_all": {}}}
        results = es.conn.search(index=es.index, body=query)

    # except ElasticHttpNotFoundError:
    #    # No documents present in store. Don't worry about it there's nothing
    #    # to search
    #    results = dict(
    #        hits=dict(hits=[], total=0),
    #        took=0,
    #    )

    hit = []
    conn = db().conn()
    for i in results['hits']['hits']:
        query = dict(_id=i['_id'])
        fields = conn.documents.find_one(query)['fields']
        if formatType == u'sdk':
            for key, value in fields.items():
                if not isinstance(value, list):
                    fields[key] = [value]
        hit.append({'id': i['_id'], 'fields': fields})

    rc = {
        "rank": "-text_relevance",
        "match-expr": u"(label '{0}')".format(qstring),
        "hits": {
            "found": results['hits']['total']['value'],
            "start": 0,
            "hit": hit
        },
        "info": {
            "rid": binascii.hexlify(os.urandom(40)).decode(),
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
        for doc in to_load:
            conn.documents.update({'_id': doc['id']}, doc, True)
            add_to_elasticsearch(doc)

    if to_remove:
        # Recover the documents that have been removed in this upload and
        # store it on the removed list.
        for doc in to_remove:
            doc_id = doc['id']
            query = dict(_id=doc_id)
            found = conn.documents.find_one(query)
            if found:
                log.debug("adding to remove store: '{0}'".format(query))
                conn.documents_removed.insert(found)
                conn.documents.remove(query)
                remove_from_elasticsearch(doc)

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

    # conn = db().conn()
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
    # Remove al of the documents from elasticsearch as well.
    get_es().hard_reset()
    log.warn("All indexes removed from elasticsearch.")
