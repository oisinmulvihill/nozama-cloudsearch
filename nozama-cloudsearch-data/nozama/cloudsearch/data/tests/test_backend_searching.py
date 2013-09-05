# -*- coding: utf-8 -*-
"""
"""
from nozama.cloudsearch.data import document


def test_basic_search(logger, mongodb):
    """Test searching the documents stored in mongodb.
    """
    assert document.all() == []

    # Set up the full text infexing.
    document.configure_field("not-used", "name", "text")

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

    rc = document.load(example_sdf)

    assert rc['status'] == 'ok'
    assert rc['adds'] == 1
    assert rc['deletes'] == 0
    assert rc['error'] == ''
    assert rc['warning'] == ''

    found = document.all()
    assert len(found) == 1

    query = dict(q="pro quad")
    results = document.search(query)

    assert len(results) != 0
    assert len(results) == 1
