# -*- coding: utf-8 -*-
"""
nozama-cloudsearch

"""
import os
import logging
import binascii

from pyramid.view import view_config

from nozama.cloudsearch.data import document
from nozama.cloudsearch.service.restfulhelpers import status_body


def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


@view_config(
    route_name='doc_search', request_method=('POST', 'GET'), renderer='json'
)
def doc_search(request):
    """Handles quering of the stored documents.

    """
    log = get_log("doc_search")

    request_id = binascii.hexlify(os.urandom(40)).decode()

    # TODO: actual query and and refine.
    #
    # return everything for the moment and emulate an Amazon search query
    # result set.
    #
    log.debug("request_id <{0}> request params <{1}>".format(
        request_id, request.params
    ))

    # Convert request.params from:
    #
    #   NestedMultiDict([
    #       (u'size', u'12'), (u'start', u'0'),
    #       (u'facet', u'price,retailer,designer,category,size,colour'),
    #       (u'facet-category-top-n', u'10000'),
    #       (u'q', u'skate board')
    #   ])
    #
    # To a handy dict:
    #
    # params = {
    #    u'facet': u'price,retailer,designer,category,size,colour',
    #    u'start': u'0', u'q': u'skate board',
    #    u'facet-category-top-n': u'10000', u'size': u'12'
    # }
    #
    # Ref:
    #  * http://docs.webob.org/en/latest/modules/webob.html
    #
    params = request.params.mixed()

    log.debug("params recovered <{0}>".format(params))

    rc = document.search(params)

    log.debug("returning <{0}> results found:\n{1}.".format(
        rc['hits']['found'],
        rc,
    ))

    return rc


@view_config(
    route_name='documents_batch', request_method='POST', renderer='json'
)
def documents_batch(request):
    """This handles the upload of documents to the cloudsearch.

    """
    log = get_log("documents_batch")

    api_version = request.matchdict['api_version']
    log.debug("Received from client API Version <{0}>".format(api_version))

    rc = document.load(request.json_body)

    log.debug("Document Batch response <{0}>".format(rc))

    return rc


@view_config(
    route_name='dev_documents', request_method='GET', renderer='json'
)
def dev_documents(request):
    """This returns documents which have been batch uploaded.

    """
    log = get_log("dev_documents")

    log.info("Returning document storage report.")

    return document.report()


@view_config(
    route_name='dev_documents', request_method='DELETE', renderer='json'
)
def remove_all(request):
    """This remove all stored documents from the system ready for a new test
    run.

    """
    log = get_log("remove_all")

    log.info("Removing all docs.")
    document.remove_all()

    log.info("All docs removed ok.")

    return status_body(message="Documents Removed OK.")
