# -*- coding: utf-8 -*-
"""
"""
import logging

from pymongo import Connection


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
            self._connection = Connection(self.host, self.port)
        return self._connection

    def conn(self):
        """Return the db connection.

        :returns: A mongodb Connection instance.

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
