# -*- coding: utf-8 -*-
"""
nozama-cloudsearch

"""
import pkg_resources

from pyramid.view import view_config


@view_config(route_name='home', request_method='GET', renderer='json')
@view_config(route_name='ping', request_method='GET', renderer='json')
def status(request):
    """This is used to 'ping' the web service to check if its running.

    :returns: a status dict which the configured view will return as JSON.

    The dict has the form::

        dict(
            status="ok",
            name="<project name>",
            version="<egg version of nozama.cloudsearch.service>"
        )

    """
    pkg = pkg_resources.get_distribution('nozama-cloudsearch')

    return dict(
        status="ok",
        name="nozama-cloudsearch",
        version=pkg.version,
    )
