# -*- coding: utf-8 -*-
"""
"""
from nozama.cloudsearch.data import document


def test_basic_search(logger, mongodb, elastic):
    """Test searching the documents stored in mongodb.
    """
    assert document.all() == []

    # Set up the full text infexing.
    document.configure_field("mydomain", "name", "text")
    #document.configure_field("mydomain", "designer", "text")

    doc = {
        "designer": "GearPro",
        "price": 12.60,
        "retailer": "MyShoppe",
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

    doc2 = {
        "designer": "GearPro",
        "price": 12.60,
        "retailer": "MyShoppe",
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
        },
        {
            "lang": "en",
            "fields": doc2,
            "version": 1376497963,
            "type": "add",
            "id": 1247
        }
    ]

    rc = document.load(example_sdf)
    assert rc['status'] == 'ok'
    assert rc['adds'] == 2

    # return all:
    results = document.search()
    assert results['hits']['found'] == 2
    assert results['hits']['hit'] == ['1247', '1246']

    # return a specific one:
    query = dict(q="pro quad")
    results = document.search(query)
    assert results['hits']['found'] == 1
    assert results['hits']['hit'] == ['1246']
