# -*- coding: utf-8 -*-
"""
PyTest Fixtures to aid in REST API validation. The test_server fixture will
run a test instance which can by the used to run tests.

Oisin Mulvihill
2013-08-22

"""
import os
import sys
import time
import socket
import logging
import tempfile
import subprocess
import http.client
import configparser
from io import StringIO
from string import Template
from urllib.parse import urlparse
from urllib.parse import urlsplit
from pkg_resources import resource_string

import pytest


def wait_for_ready(uri, retries=40, wait_period=0.5, timeout=1.0):
    """Called to wait for a web application to respond to normal requests.

    This function will attempt a HEAD request if its
    supported, otherwise it will use GET.

    :param uri: the URI of the web application on which
    it will receive requests.

    :param retries: The amount of attempts to try finding
    a free port.

    :param wait_period: The seconds to wait before attempting connection.

    :param timeout: The socket timeout to prevent blocking.

    :returns: True: the web app ready.

    """
    returned = False

    URI = uri
    # Work set up the connection for the HEAD request:
    o = urlsplit(URI)
    conn = http.client.HTTPConnection(o.hostname, o.port, timeout=timeout)

    while retries:
        retries -= 1
        try:
            # Just get the headers and not the body to speed things up.
            conn.request("HEAD", '/')
            res = conn.getresponse()
            if res.status == http.client.OK:
                # success, its ready.
                returned = True
                break

            elif res.status == http.client.NOT_IMPLEMENTED:
                # HEAD not supported try a GET instead:
                try:
                    urllib.urlopen(URI)
                except IOError:
                    # Not ready yet. I should check the exception to
                    # make sure its socket error or we could be looping
                    # forever. I'll need to use a state machine if this
                    # prototype works. For now I'm taking the "head in
                    # the sand" approach.
                    pass
                else:
                    # success, its ready.
                    returned = True
                    break

        except http.client.CannotSendRequest:
            # Not ready yet.
            pass

        except socket.error:
            # Not ready yet. I should check the exception to
            # make sure its socket error or we could be looping
            # forever. I'll need to use a state machine if this
            # prototype works. For now I'm taking the "head in
            # the sand" approach.
            pass

        time.sleep(wait_period)

    return returned


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
def mongodb(logger, request):
    """Set up a mongo connection reset and ready to roll.
    """
    from nozama.cloudsearch.data import db
    from nozama.cloudsearch.service import environ_settings
    cfg = dict(
        db_name='unittesting-db',
        port=environ_settings.MONGO_PORT(),
        host=environ_settings.MONGO_HOST(),
    )
    logger.debug("MongoDB config<{0}>".format(cfg))
    db.init(cfg)
    db.db().hard_reset()


@pytest.fixture(scope='function')
def elastic(logger, request):
    """Set up a elasticsearch connection reset and ready to roll.

    This will attempt to connect to the default elasticsearch instance
    on http://localhost:9200. Its not configurable yet.

    """
    from nozama.cloudsearch.data import db
    from nozama.cloudsearch.service import environ_settings
    cfg = dict(es_endpoint="http://{}:{}".format(
        environ_settings.ELASTICSEARCH_HOST(),
        environ_settings.ELASTICSEARCH_PORT()
    ))
    logger.debug("ElasticSearch config<{0}>".format(cfg))
    db.init_es(cfg)
    db.get_es().hard_reset()


class ServerRunner(object):
    """Start/Stop the testserver for web testing purposes.

    """
    def __init__(self, port=None, configfile=None, interface='127.0.0.1'):
        """
        """
        self.log = logging.getLogger("ServerRunner")
        self.serverPid = None
        self.serverProcess = None
        if interface:
            self.interface = interface
        else:
            self.interface = '127.0.0.1'
        if port:
            self.port = port
        else:
            # Get a free port the socket way.
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 0))
            self.port = s.getsockname()[1]
            s.close()

        self.URI = "http://%s:%s" % (self.interface, self.port)

        # Make directory to put file and other data into:
        self.test_dir = tempfile.mkdtemp()
        self.log.info("Test Server temp directory <%s>" % self.test_dir)

        # Get template in the tests dir:
        self.temp_config = os.path.join(self.test_dir, 'test_cfg.ini')

        # The service to run with the rendered configuration:
        self.cmd = "pserve {0}".format(self.temp_config)

        self.test_cfg = resource_string(__name__, 'test_cfg.ini.template')
        cfg_tmpl = Template(self.test_cfg.decode())
        data = dict(
            interface=self.interface,
            port=int(self.port),
        )
        data = cfg_tmpl.substitute(data)
        with open(self.temp_config, "wb") as fd:
            fd.write(data.encode())
        self.config = configparser.ConfigParser()
        self.config.readfp(StringIO(data))

        config = configparser.ConfigParser(dict(here=self.test_dir))
        self.log.info("Setting up common db from <%s>" % self.temp_config)
        config.read(self.temp_config)

    def cleanup(self):
        """Clean up temp files and directories.
        """
        for f in [self.temp_config]:
            try:
                os.remove(f)
            except OSError:
                os.system('rm {0}'.format(f))
        try:
            os.removedirs(self.test_dir)
        except OSError:
            os.system('rm -rf {0}'.format(self.test_dir))

    def start(self):
        """Spawn the web app in testserver mode.

        After spawning the web app this method will wait
        for the web app to respond to normal requests.

        """
        self.log.info(
            "start: running <%s> in <%s>." % (self.cmd, self.test_dir)
        )

        # Spawn as a process and then wait until
        # the web server is ready to accept requests.
        #
        self.serverProcess = subprocess.Popen(
            args=self.cmd,
            shell=True,
            cwd=self.test_dir,
        )
        pid = self.serverProcess.pid

        if not self.isRunning():
            raise SystemError("%s did not start!" % self.cmd)

        # self.log.debug("start: waiting for '%s' readiness." % self.URI)
        wait_for_ready(self.URI + "/ping", retries=10)

        return pid

    def stop(self):
        """Stop the server running."""
        self.log.info("stop: STOPPING Server.")

        # Stop:
        if self.isRunning():
            self.serverProcess.terminate()
            os.waitpid(self.serverProcess.pid, 0)

        # Make sure its actually stopped:
        if sys.platform.startswith('win'):
            subprocess.call(
                args="taskkill /F /T /IM pserve.exe",
                shell=True,
            )
        else:
            subprocess.call(
                args=(
                    'ps -a | grep -v grep | grep "pserve*" '
                    '| awk \'{print "kill -15 "$1}\' | sh'
                ),
                shell=True,
            )

    def isRunning(self):
        """Called to testserver

        returned:
            True - its running.
            False - its not running.

        """
        returned = False
        process = self.serverProcess

        if process and process.poll() is None:
            returned = True

        return returned


@pytest.fixture(scope='session')
def test_server(request):
    """Pytest fixture to run a test instance of the service.

    """
    log = logging.getLogger("test_server")

    test_server = ServerRunner()

    # Set up the client side rest api and set it up with the URI of the
    # running test service.
    from nozama.cloudsearch.client.rest import CloudSearchService

    log.debug("server: setting up REST client API for URI '{0}'.".format(
        test_server.URI
    ))

    # Attach to the server object:
    test_server.api = CloudSearchService(uri=test_server.URI)

    def teardown():
        """Stop running the test instance."""
        log.debug("teardown: '{0}' stopping instance.".format(test_server.URI))
        test_server.stop()
        test_server.cleanup()
        log.debug("teardown: '{0}' stop and cleanup called OK.".format(
            test_server.URI
        ))

    request.addfinalizer(teardown)

    log.debug("server: starting instance.")
    test_server.start()

    return test_server
