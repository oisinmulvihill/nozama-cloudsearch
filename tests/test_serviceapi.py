# -*- coding: utf-8 -*-
"""
Tests to verify the REST interface of the nozama-cloudsearch.

Oisin Mulvihill
2013-08-22

"""
import pkg_resources


def test_service_is_running(test_server):
    """Test the service is running and the status it returns.
    """
    response = test_server.api.ping()

    pkg = pkg_resources.get_distribution("nozama-cloudsearch")

    # print response

    assert response["status"] == "ok"
    assert response['name'] == 'nozama-cloudsearch'
    assert response['version'] == pkg.version


def test_batch_document_upload_add(test_server):
    """Test the /documents/batch API.
    """
    test_server.api.remove_all()
    report = test_server.api.report()
    assert report['documents'] == []
    assert report['documents_removed'] == []

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

    report = test_server.api.report()

    # print "report"
    # print report
    # print

    found = report['documents']

    assert len(found) == 1
    assert found[0]['id'] == '1246'
    assert found[0]['_id'] == '1246'
    assert found[0]['lang'] == 'en'
    # type should have been stripped:
    assert 'type' not in found[0]
    assert found[0]['version'] == '1376497963'
    assert found[0]['fields']['name'] == "Pro Quad Clamp Purple"

    test_server.api.remove_all()
    report = test_server.api.report()
    found = report['documents']
    assert len(found) == 0
