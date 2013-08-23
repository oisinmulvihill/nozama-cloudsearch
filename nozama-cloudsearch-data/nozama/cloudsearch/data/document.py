# -*- coding: utf-8 -*-
"""
"""
import logging

from nozama.cloudsearch.data.db import db


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
        ["add", "remove"], not_empty=True, strip=True,
    )


DOC_SCHEMA = DocSchema()


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
            to_remove.append(doc)

    if to_load:
        log.debug("bulk loading: '{0}' document(s)".format(len(to_load)))
        conn.documents.insert(to_load)

    if to_remove:
        doc_ids = [doc['_id'] in to_remove]
        log.debug("bulk removing: '{0}' documents(s)".format(len(doc_ids)))
        conn.documents.remove(doc_ids)

    rc = dict(
        status='ok',
        adds=len(to_load),
        deletes=len(to_remove),
        error='',
        warning='',
    )

    return rc


def remove_all():
    """Remove all store documents.
    """
    log = get_log('remove_all')
    conn = db().conn()
    conn.documents.drop()
    log.warn("all documents have been removed.")
