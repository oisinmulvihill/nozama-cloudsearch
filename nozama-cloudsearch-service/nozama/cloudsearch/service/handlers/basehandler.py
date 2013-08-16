# -*- coding: utf-8 -*-
"""
This provides request handler functionality all other handlers will use.

Oisin Mulvihill
2013-08-16T14:18:34

"""
import json
import logging
import traceback

import tornado.ioloop
import tornado.web

from nozama.cloudsearch.service.responseutil import utf8_str
from nozama.cloudsearch.service.responseutil import gen_reponse


class BaseHandler(tornado.web.RequestHandler):
    """Common request handler.

    Based on https://github.com/nws-cip/cip-metrics/blob/master/ \
        src/api/lib/api/requesthandlermixin.py

    """
    log = logging.getLogger("%s.%s" % (__name__, "BaseHandler"))

    def get_logger_args(self):
        """Return a dict of information used for logging request information.

        :returns: A dict

        E.g.::
            {
                'ip': 'remoter ip address',
                'userid': 'user name ' or None
            }

        """
        return {
            'ip': self.request.remote_ip,
            'userid': getattr(self, 'user', None)
        }

    logger_args = property(get_logger_args)

    def prepare(self):
        """Based on the Content-Type header interpret the request body.

        Ref:
          * https://github.com/facebook/tornado/wiki/Frequently-asked-questions

        Content-Type: 'application/json' the 'self.json_body' will contain
        the json.loads(self.request.body). The json_body will be an empty
        dict if the Content-Type is not JSON.

        The common approach to REST services is

        """
        self.json_body = {}
        body = self.request.body

        self.log.debug("prepare: raw request: <%s>" % body)

        if self.request.headers.get("Content-Type") == "application/json":
            try:
                if body:
                    self.json_body = json.loads(body)

            except ValueError:
                msg = "prepare: decode JSON error for <%s>" % body
                self.log.exception(msg)

    def write(self, data, status='ok', message=''):
        """Wrap the data in the gen_response() object return.

        Override to set the Content-Type header.

        This will set the encoding of the returned JSON to UTF-8.

        """
        data = gen_reponse(data, status, message)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        super(BaseHandler, self).write(data)

    def write_error(self, error_code, message=None, **kwargs):
        """Override the error writing function to output in JSON format.

        :param error_code: HTTP Error code.
        :param message: Error message to ouput.

        """
        ret = dict(error="", trace="", code=error_code)

        if 'exc_info' in kwargs:
            error, detail, tb = kwargs['exc_info']

            #import pdb ; pdb.set_trace()

            if error.__name__ == "HTTPException":
                # Set the error code properly for deliberate REST / HTTP error
                # codes raised from handlers.
                #
                ret['error'] = utf8_str(detail.args[1])
                ret['code'] = detail.args[0]

            else:
                # Unknown exception, roll with it:
                ret['error'] = utf8_str(error)
                ret['trace'] = "".join(traceback.format_tb(tb))

        # Log the error
        msg = "%(error)s %(code)s %(trace)s" % ret
        self.log.error(msg)
        #self.application.log.log_error(msg, logger_args=self.logger_args)

        # Output the error
        self.log.debug("setting error code <%d>" % ret['code'])
        self.set_status(ret['code'])

        # Generate the error body:
        self.write(ret['error'], status='error', message=msg)

    def on_finish(self, handler=None):
        """Override on_finish function to log all requests.

        :param handler: The handler used to fufil the request

        """
        msg = "%s %s %s" % (
            self.get_status(),
            self.request.method,
            self.request.uri
        )
        self.log.info(msg)
        #self.application.log.log_info(msg, logger_args=self.logger_args)
