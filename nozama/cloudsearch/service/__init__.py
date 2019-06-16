# -*- coding: utf-8 -*-
"""
REST Service 'nozama-cloudsearch'

"""
import os
import logging

from pyramid.config import Configurator

from nozama.cloudsearch.data import db
from nozama.cloudsearch.service import docs
from nozama.cloudsearch.service import restfulhelpers
from nozama.cloudsearch.service import environ_settings


def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    log = get_log('main')

    config = Configurator(settings=settings)

    cfg = dict(
        db_name=environ_settings.MONGO_DBNAME(),
        port=environ_settings.MONGO_PORT(),
        host=environ_settings.MONGO_HOST(),
    )
    log.debug("MongoDB config<{0}>".format(cfg))
    db.init(cfg)

    cfg = dict(
        es_endpoint=settings.get(
            "elasticsearch.endpoint",
            "http://{}:{}".format(
                environ_settings.ELASTICSEARCH_HOST(),
                environ_settings.ELASTICSEARCH_PORT()
            )
        ),
    )
    log.debug("ElasticSearch config<{0}>".format(cfg))
    db.init_es(cfg)

    # Custom 404 json response handler. This returns a useful JSON
    # response in the body of the 404.
    # XXX this is conflicting
    # config.add_view(restfulhelpers.notfound_404_view, context=HTTPNotFound)

    not_found = restfulhelpers.xyz_handler(404)
    config.add_view(not_found, context='pyramid.exceptions.NotFound')

    bad_request = restfulhelpers.xyz_handler(400)
    config.add_view(
        bad_request,
        context='pyramid.httpexceptions.HTTPBadRequest'
    )

    # Host out the sphinx documentation that are generated and put into
    # the docs dir.
    d_path = os.path.abspath(docs.__path__[0])
    config.add_static_view('docs', d_path)

    # Javascript/CSS/etc
    config.add_static_view('static', 'static', cache_max_age=3600)

    # handled by ping at the moment. I must do a proper amazom cloudsearch
    # root.
    config.add_route(
        'home', '/'
    )

    # Amazon CloudSearch REST interface routes:
    #
    config.add_route(
        'documents_batch', '/{api_version}/documents/batch'
    )

    config.add_route(
        'doc_search', '/{api_version}/search'
    )

    # Testing URL(s) query the results of cloud search operations.
    #
    config.add_route('dev_documents', '/dev/documents')

    # Maps to the status page:
    config.add_route('ping', '/ping')

    # Pick up the views which set up the views automatically:
    #
    config.scan("nozama.cloudsearch.service")

    # Make the pyramid app I'll then wrap in other middleware:
    app = config.make_wsgi_app()

    # RESTful helper class to handle PUT, DELETE over POST requests:
    app = restfulhelpers.HttpMethodOverrideMiddleware(app)

    # Should be last to catch all errors of below wsgi apps. This
    # returns useful JSON response in the body of the 500:
    app = restfulhelpers.JSONErrorHandler(app)

    return app
