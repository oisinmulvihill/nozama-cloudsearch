# -*- coding: utf-8 -*-
"""
"""
import logging
from urllib.parse import urljoin

from pymongo import MongoClient
from elasticsearch import Elasticsearch


class DB(object):
    """An lightwrapper around a mongodb connection.

    The init is given the configuration dict::

        dict(
            db_name='<name>',  # test-db is default.
            port=<mongodb tcp port>,  # 27012 by default.
            host=<mongodb host address>,  # localhost by default.
        )

    Create this class and then call instances db property to
    start using.

    The db_name and host must be strings and they will be stripped
    of trailing whitespace prior to use.

    """
    def __init__(self, config={}):
        self.log = logging.getLogger("%s.DB" % __name__)
        self.config = config
        self.db_name = config.get("db_name", "nozama-cloudsearch").strip()
        self.port = int(config.get("port", 27017))
        self.host = config.get("host", "localhost").strip()
        self._connection = None

    def mongo_conn(self):
        """Returns a mongodb connection not tied to a database."""
        if not self._connection:
            self._connection = MongoClient(self.host, self.port)
        return self._connection

    def conn(self):
        """Return the db connection.

        :returns: A mongodb MongoClient instance.

        """
        return self.mongo_conn()[self.db_name]

    def hard_reset(self):
        """Remove the database from mongo clearing out all contents.

        This is used mainly in testing.

        """
        self.mongo_conn().drop_database(self.db_name)


#
__db = None


def init(config={}):
    """Set up the default DB instance a call to get_db() will return.

    :param config: See DB() docs for config dict fields.

    :returns: None.

    """
    global __db
    __db = DB(config)


def db():
    """Recover the current configured DB instance.

    If no default instance is configured then ValueError will be raised.

    :returns: The DB instance configured through init().

    """
    if not __db:
        raise ValueError("No DB instance configured! Call init() first.")
    return __db


__es = None


class ElasticSearchHelper(object):
    """
    """
    def __init__(self, config={}):
        """
        :param config: A dict containing at least es_endpoint field.

        .. code-block:: python

            {
                "es_endpoint": "http://localhost:9200",
                "es_namespace": "test1"
            }

        """
        self.log = logging.getLogger("%s.ElasticSearchHelper" % __name__)
        self.base_uri = config.get('es_endpoint', 'http://localhost:9200')
        self.log.info(
            "Using ElasticSearch Endpoint '{0}'".format(self.base_uri)
        )
        self.namespace = config.get('es_namespace', '')
        self.index = '{0}documents'.format(self.namespace)
        self.doc_type = 'fields'
        self.document_path = '/{0}/{1}'.format(self.index, self.doc_type)
        self.search_path = '{0}/_search'.format(self.document_path)
        self.document_uri = urljoin(self.base_uri, self.document_path)
        self.search_uri = urljoin(self.base_uri, self.search_path)
        self.log.info(
            "document_uri is '{0}' search_uri is '{1}'".format(
                self.document_uri,
                self.search_uri
            )
        )
        self.conn = Elasticsearch(self.base_uri)

    def hard_reset(self):
        """Remove all indexed documents from search ready for a new test run.
        """
        url = urljoin(self.base_uri, self.document_path)

        self.log.warn(
            "hard_reset: removing all content from {0}".format(url)
        )

        self.conn.indices.delete(index=self.index, ignore=[404, 400])
        self.conn.indices.create(index=self.index, ignore=400)

        self.log.warn(
            "hard_reset: all content removed from {0} OK.".format(url)
        )


def init_es(config={}):
    """Set up the default DB instance a call to get_db() will return.

    :param config: See DB() docs for config dict fields.

    :returns: None.

    """
    global __es
    __es = ElasticSearchHelper(config)


def get_es():
    """Recover the elastic search connection helper.

    :returns: The ElasticSearchHelper instance configured through init().

    """
    if not __es:
        raise ValueError(
            "No ElasticSearchHelper instance configured! Call init() first."
        )
    return __es
