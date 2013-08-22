# -*- coding: utf-8 -*-
"""
nozama-cloudsearch-service

"""
import logging

from pyramid.view import view_config


def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


@view_config(
    route_name='documents_batch', request_method='POST', renderer='json'
)
def documents_batch(request):
    """This handles the upload of documents to the cloudsearch.

    """
    return []


@view_config(
    route_name='dev_documents', request_method='POST', renderer='json'
)
def dev_documents(request):
    """This returns documents which have been batch uploaded.

    """
    return []
