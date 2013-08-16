# -*- coding: utf-8 -*-
"""
Tests to verify the REST interface provided by a running test tornado instance.

Oisin Mulvihill
2013-08-16T14:18:34

"""
import urllib
import unittest
import pkg_resources

from nozama.cloudsearch.client import rest
from nozama.cloudsearch.service.tests import svrhelp


def setup_module():
    """Start the test app running on module set up and stop it
    running on teardown.

    """
    svrhelp.setup_module()

    # Create the db now the server is running in its own dir.
    #db.init(...)

teardown_module = svrhelp.teardown_module


class RESTSegmentTC(unittest.TestCase):

    def setUp(self):
        # Set up the REST API client:
        self.api = rest.CloudsearchService(svrhelp.serviceapp.URI)

    def test_service_is_running(self):
        """Test the service is running and the status it returns.
        """
        response = self.api.ping()
        self.assertEquals(response["status"], "ok")

        report = response['result']
        self.assertTrue("name" in report)
        self.assertTrue("version" in report)

        pkg = pkg_resources.get_distribution("nozama-cloudsearch-service")

        self.assertEquals(report['name'], 'nozama-cloudsearch-service')
        self.assertEquals(report['version'], pkg.version)
