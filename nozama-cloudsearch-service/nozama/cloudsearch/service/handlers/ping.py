# -*- coding: utf-8 -*-
"""
This provides a URL you can call to check if the service is present
and its current version.

Oisin Mulvihill
2013-08-16T14:18:34

"""
import logging
import pkg_resources

from nozama.cloudsearch.service.handlers.basehandler import BaseHandler


class PingHandler(BaseHandler):

    log = logging.getLogger("%s.PingHandler" % __name__)

    def get(self):
        """This will return the package name and version response.

        :returns: a gen_response(...) wrapped dict.

        E.g.::

            {
                'name': 'nozama-cloudsearch-service',
                'version': 'x.y.z',
            }

        """
        pkg = pkg_resources.get_distribution("nozama-cloudsearch-service")

        rc = {
            'name': 'nozama-cloudsearch-service',
            'version': pkg.version,
        }

        self.log.debug("ping! returning <%s>" % rc)
        self.write(rc)


URLS = [
    (r"/ping", PingHandler),
]
