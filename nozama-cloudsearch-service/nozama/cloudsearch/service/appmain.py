# -*- coding: utf-8 -*-
"""
The Tornado REST Service.

Oisin Mulvihill
2013-08-16T14:18:34

"""
import logging

import tornado.ioloop
import tornado.web

from nozama.cloudsearch.service.handlers import ping


def generate_urlspace():
    """This generates the URLS passed to tornado.web.Application(...)

    :returns: List of urls.

    """
    URLS = []

    # The complete map of supported URLs. Each module will have its own URLS
    # close to the definition of the Handlers it provides. This could probably
    # done more automatically later:

    URLS.extend(ping.URLS)

    return URLS


def tornado_main(cfg, options={}):
    """Create the tornado app with given config and run forever.

    :param cfg: This is a dict of fields from the configuration.

    E.g.::

        cfg = dict(
            # default:
            port=63833
        )

    :param options: A dict of options which is empty by default.

    E.g.::

        options = dict(
            create_schema = False (default) | True
        )

        If this is set (create_schema = True) then the hbase schema
        will be created. The program will exit after a schema creation
        run.

    """
    log = logging.getLogger("%s.tornado_main" % __name__)

    port = int(cfg.get('port', 63833))

    urls = generate_urlspace()
    import pprint
    log.debug("URL Space:\n%s" % pprint.pformat(urls))

    create_schema = options.get("create_schema", False)

    if create_schema:
        log.warn("Creating hbase schema.")
        db.get_db().setUp()
        log.info("Done.")

    else:
        application = tornado.web.Application(urls)
        application.listen(port)
        log.info("Running: port <%d>." % port)
        tornado.ioloop.IOLoop.instance().start()
