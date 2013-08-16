# -*- coding: utf-8 -*-
"""
(c) Oisin Mulvihill: Taken from my projects and I release it
under BSD license. Its ok to use it in this here and in other
projects without restriction.

"""
import os
import sys
import logging
import StringIO
import tempfile
import subprocess
import ConfigParser
from string import Template
from pkg_resources import resource_string

from evasion.common import net


def get_log(extra=None):
    m = __name__ if not extra else "%s.%s" % (__name__, extra)
    return logging.getLogger(m)


class ServerRunner(object):
    """Start/Stop the testserver for web testing purposes.
    """
    def __init__(self, port=None, configfile=None, interface='localhost'):
        """
        """
        self.log = get_log("ServerRunner")
        self.serverPid = None
        self.serverProcess = None
        if interface:
            self.interface = interface
        else:
            self.interface = '127.0.0.1'
        if port:
            self.port = port
        else:
            self.port = net.get_free_port()

        self.URI = "http://%s:%s" % (self.interface, self.port)

        # Make directory to put file and other data into:
        self.test_dir = tempfile.mkdtemp()
        self.log.info("Test Server temp directory <%s>" % self.test_dir)

        # Get template in the tests dir:
        self.temp_config = os.path.join(self.test_dir, 'test_cfg.ini')

        # The service to run with the rendered configuration:
        self.cmd = "cloudsearch_service --config=%s" % self.temp_config

        self.test_cfg = resource_string(__name__, 'test_cfg.ini.tmpl')
        cfg_tmpl = Template(self.test_cfg)
        data = cfg_tmpl.substitute(
            interface=self.interface,
            port=self.port,
        )
        with open(self.temp_config, "wb") as fd:
            fd.write(data)
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(StringIO.StringIO(data))

        config = ConfigParser.ConfigParser(dict(here=self.test_dir))
        self.log.info("Setting up common db from <%s>" % self.temp_config)
        config.read(self.temp_config)

    def cleanup(self):
        """Clean up temp files and directories.
        """
        for f in [self.temp_config]:
            try:
                os.remove(f)
            except OSError:
#                os.system("rm %f" % f)
# Gives error: "TypeError: float argument required, not str"
                os.system('rm {}'.format(f))
        try:
            os.removedirs(self.test_dir)
        except OSError:
#            os.system("rm -rf %f" % self.test_dir)
            os.system('rm -rf {}'.format(self.test_dir))

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

        #self.log.debug("start: waiting for '%s' readiness." % self.URI)
        #net.wait_for_ready(self.URI + "/ping", timeout=5)
        import time
        time.sleep(2)

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
                args="taskkill /F /T /IM cloudsearch_service.exe",
                shell=True,
            )
        else:
            subprocess.call(
                args=(
                    'ps -a | grep -v grep | grep "cloudsearch_ser*" '
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


# Ok, tie the above together:
#
serviceapp = None


def setup_module():
    """Recover the configuration from TESTING_CONFIG and run the serviceapp on
    a free port.

    This will wait until the web app starts to respond before returning.

    """
    log = get_log()
    global serviceapp
    serviceapp = ServerRunner()
    log.debug("setup_module: starting web app.")
    serviceapp.start()
    log.debug("setup_module: running.")


def teardown_module():
    """Stop running the test serviceapp if an instance was set up."""
    log = get_log()
    global serviceapp

    if serviceapp:
        log.debug(
            "teardown_module: stopping test serviceapp '%s'." % serviceapp.URI
        )
        serviceapp.stop()
        serviceapp.cleanup()
        serviceapp = None
