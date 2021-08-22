# -*- coding: utf-8 -*-
"""
"""
from nozama.cloudsearch.data import document


def test_document_add(logger, elastic, mongodb):
    """Test mongo document API.
    """
    assert document.all() == []

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
    assert found[0]['id'] == '1246'
    assert found[0]['_id'] == '1246'
    assert found[0]['lang'] == 'en'
    # type should have been stripped:
    assert 'type' not in found[0]
    assert found[0]['version'] == '1376497963'
    assert found[0]['fields']['name'] == "Pro Quad Clamp Purple"

    document.remove_all()
    assert len(document.all()) == 0


def test_remove_on_emtpy(logger, mongodb):
    """Test a remove sdf on an empty db causes no problems.
    """
    assert document.all() == []

    example_sdf = [
        {
            "type": "delete",
            "id": "1246",
            "version": 2
        }
    ]
    rc = document.load(example_sdf)

    assert rc['status'] == 'ok'
    assert rc['adds'] == 0
    assert rc['deletes'] == 1
    assert rc['error'] == ''
    assert rc['warning'] == ''

    found = document.all()
    assert len(found) == 0

    report = document.report()

    assert len(report['documents_removed']) == 0
    assert len(report['documents']) == 0


def test_add_remove(logger, mongodb):
    """Test add and removing of documents via the batch upload sdf.
    """
    assert document.all() == []

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

    example_add_sdf = [
        {
            "lang": "en",
            "fields": doc,
            "version": 1376497963,
            "type": "add",
            "id": 1246
        }
    ]

    rc = document.load(example_add_sdf)

    assert rc['status'] == 'ok'
    assert rc['adds'] == 1
    assert rc['deletes'] == 0
    assert rc['error'] == ''
    assert rc['warning'] == ''

    report = document.report()

    assert len(report['documents_removed']) == 0
    assert len(report['documents']) == 1
    doc = report['documents'][0]
    assert doc["fields"]["name"] == "Pro Quad Clamp Purple"

    # Now remove the document from the store:
    #
    example_remove_sdf = [
        {
            "type": "delete",
            "id": "1246",
            "version": 2
        }
    ]
    rc = document.load(example_remove_sdf)

    assert rc['status'] == 'ok'
    assert rc['adds'] == 0
    assert rc['deletes'] == 1
    assert rc['error'] == ''
    assert rc['warning'] == ''

    found = document.all()
    assert len(found) == 0

    report = document.report()

    assert len(report['documents_removed']) == 1
    assert len(report['documents']) == 0
    doc = report['documents_removed'][0]
    assert doc["fields"]["name"] == "Pro Quad Clamp Purple"

    # Clear out the remove and delete record of all documents:
    #
    document.remove_all()
    report = document.report()
    assert len(document.all()) == 0
    assert len(report['documents_removed']) == 0
    assert len(report['documents']) == 0


def test_remove_then_search(logger, mongodb):
    """Test search after a removal of a document.
    """
    assert document.all() == []

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

    example_add_sdf = [
        {
            "lang": "en",
            "fields": doc,
            "version": 1376497963,
            "type": "add",
            "id": 1246
        }
    ]

    rc = document.load(example_add_sdf)

    assert rc['status'] == 'ok'
    assert rc['adds'] == 1
    assert rc['deletes'] == 0
    assert rc['error'] == ''
    assert rc['warning'] == ''

    report = document.report()

    assert len(report['documents_removed']) == 0
    assert len(report['documents']) == 1
    doc = report['documents'][0]
    assert doc["fields"]["name"] == "Pro Quad Clamp Purple"

    # Now remove the document from the store:
    #
    example_remove_sdf = [
        {
            "type": "delete",
            "id": "1246",
            "version": 2
        }
    ]
    rc = document.load(example_remove_sdf)

    assert rc['status'] == 'ok'
    assert rc['adds'] == 0
    assert rc['deletes'] == 1
    assert rc['error'] == ''
    assert rc['warning'] == ''

    found = document.all()
    assert len(found) == 0

    report = document.report()

    assert len(report['documents_removed']) == 1
    assert len(report['documents']) == 0
    doc = report['documents_removed'][0]
    assert doc["fields"]["name"] == "Pro Quad Clamp Purple"

    # Now search for the document:
    #
    found = document.search({ 'q': 'Pro Quad Clamp Purple' })
    hits = found['hits']

    assert hits['found'] == 0

