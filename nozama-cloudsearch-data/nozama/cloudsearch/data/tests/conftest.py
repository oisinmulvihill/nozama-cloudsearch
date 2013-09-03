# -*- coding: utf-8 -*-
"""
"""
import logging

import pytest


@pytest.fixture(scope='session')
def logger(request):
    """Set up a root logger showing all entries in the console.
    """
    log = logging.getLogger()
    hdlr = logging.StreamHandler()
    fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt)
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)
    log.propagate = False

    return log


@pytest.fixture(scope='function')
def mongodb(request):
    """Set up a mongo connection reset and ready to roll.
    """
    from nozama.cloudsearch.data import db
    db.init(dict(db_name='unittesting-db'))
    db.db().hard_reset()
