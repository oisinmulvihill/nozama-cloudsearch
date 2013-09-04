# -*- coding: utf-8 -*-
"""
Test to verify my implementation of the search API.

Oisin Mulvihill
2013-08-22

"""
import pytest


@pytest.mark.xfail
def test_searching(test_server):
    """Currently searching returns all documents uploading with no filtering.

    This test will fail as the search is not restricting. I'm marking it as
    failing so I know to fix this.

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
    found = report['documents']
    assert len(found) == 1
    assert found[0]['id'] == '1246'
    assert found[0]['_id'] == '1246'
    assert found[0]['lang'] == 'en'
    assert found[0]['version'] == '1376497963'
    assert found[0]['fields']['name'] == "Pro Quad Clamp Purple"

    # It doesn't matter whats entered here as no filtering is done currently. I
    # will implement searching behaviour as I need it for the apps I'm working
    # with.
    #
    results = test_server.api.search('skate board')
    assert len(results['hits']['found']) == 0
