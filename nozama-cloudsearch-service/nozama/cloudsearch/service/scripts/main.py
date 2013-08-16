# -*- coding: utf-8 -*-
"""
This provides the "main" of the cloudsearch_service.

Oisin Mulvihill
2012-08-21

"""
import os
import sys
import logging
import ConfigParser
import logging.config
from optparse import OptionParser

from nozama.cloudsearch.service.appmain import tornado_main


def logtoconsolefallback(log):
    """Configure the given logger to output to console.

    This is used as failover logging if the configuration doesn't
    provide any valid logging configuration.

    """
    hdlr = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)
    log.propagate = False


def main():
    """This is the program main that setup.py will use to convert into the
    program 'audience_service'. This will recover configuration, set up logging
    and do other useful house keeping.

    """
    cfg_file = "config.ini"

    log = logging.getLogger()
    parser = OptionParser()

    parser.add_option(
        "--config", action="store", dest="config_filename",
        default=cfg_file,
        help="This configuration file to use at run time (default %s)." % (
            cfg_file
        ),
    )

    (options, args) = parser.parse_args()

    if not os.path.isfile(options.config_filename):
        sys.stderr.write(
            "The config file name '%s' wasn't found" % options.config_filename
        )
        sys.exit(1)

    try:
        # Recover logging from the configuration file:
        logging.config.fileConfig(options.config_filename)

    except ConfigParser.NoSectionError:
        logtoconsolefallback(log)
        log.warn(
            "No logging found in configuration. Using console logging."
        )

    config = ConfigParser.ConfigParser()
    log.debug("config: recovering config from <%s>" % options.config_filename)
    config.read(options.config_filename)
    cfg = dict(config.items("cloudsearch-service"))

    try:
        tornado_main(cfg, {})

    except KeyboardInterrupt:
        log.info("Ctrl-C caught, exit time.")
