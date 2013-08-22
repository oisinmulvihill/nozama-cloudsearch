# -*- coding: utf-8 -*-
"""
nozama-cloudsearch-service

"""
import logging

from pyramid.view import view_config

from nozama.cloudsearch.service.restfulhelpers import status_body

def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


@view_config(
    route_name='documents_batch', request_method='POST', renderer='json'
)
def documents_batch(request):
    """This handles the upload of documents to the cloudsearch.

    """
    log = get_log("documents_batch")

    api_version = request.matchdict['api_version']
    log.debug("Received from client API Version <{0}>".format(api_version))

    return []


@view_config(
    route_name='dev_documents', request_method='POST', renderer='json'
)
def dev_documents(request):
    """This returns documents which have been batch uploaded.

    """
    return []


@view_config(
    route_name='dev_documents', request_method='DELETE', renderer='json'
)
def remove_all_docs(request):
    """This remove all stored documents from the system ready for a new test
    run.

    """
    return status_body(message="Documents Removed OK.")
