# -*- coding: utf-8 -*-
"""
Tests to verify the REST interface of the nozama-cloudsearch-service.

Oisin Mulvihill
2013-08-22

"""
#import pytest
import pkg_resources


def test_service_is_running(test_server):
    """Test the service is running and the status it returns.
    """
    response = test_server.api.ping()

    pkg = pkg_resources.get_distribution("nozama-cloudsearch-service")

    print response

    assert response["status"] == "ok"
    assert response['name'] == 'nozama-cloudsearch-service'
    assert response['version'] == pkg.version


def test_batch_document_upload_add(test_server):
    """Test the /documents/batch API.
    """
    test_server.api.remove_all_documents()
    assert test_server.api.all_documents() == []

    # upload and example document
    doc = {
        "designer": "98",
        "price": 1195,
        "retailer": "",
        "brand_id": [
            7017
        ],
        "size": [],
        "category": "",
        "name": "Pro Quad Clamp Purple",
        "colour": [],
        "brand": "98",
        "created_at": 1376391294
    }

    example_sdf = [
        {
            "lang": "en",
            "fields": doc,
            "version": 1376497963,
            "type": "add",
            "id": 1246
        }
    ]
    test_server.api.batch_upload(example_sdf)

    assert test_server.api.all_documents() == [doc]
