# -*- coding: utf-8 -*-
"""
"""
import json


def tornadoargs_to_dict(arguments):
    return dict((k, v[-1]) for k, v in arguments.iteritems())


def utf8_str(msg):
    """Convert to the given msg from unicode to a utf-8 string. If its not
    unicode just use str() on it.
    """
    if isinstance(msg, unicode):
        msg = msg.encode('utf-8')
    else:
        msg = str(msg)
    return msg


def gen_reponse(data, status="ok", message="", to_json=True):
    """Generate a response dict.

    :param data: Anything the caller expects back as a result of the request.

    :param status: "ok" (default) or "error".

    :param message: "" (default) optional message for status = "error".

    :param to_json: True (default) | False, returned dict becomes JSON if True.

    :returns: a dict or json dump of dict.

    E.g.::

        rc = dict(
            result=data,
            status=status,
            message="",
        )

    """
    if isinstance(status, unicode):
        status = status.encode('utf-8')
    else:
        message = str(status)

    if isinstance(message, unicode):
        message = message.encode('utf-8')
    else:
        message = str(message)

    rc = dict(
        result=data,
        status=status,
        message=message,
    )

    if to_json:
        rc = json.dumps(rc)

    return rc
