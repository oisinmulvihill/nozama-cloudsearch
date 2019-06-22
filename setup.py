# -*- coding: utf-8 -*-
"""
Setuptools script for content-classify-service (content.classify.service)

"""
from setuptools import setup, find_packages

Name = 'nozama-cloudsearch'
ProjectUrl = "https://github.com/oisinmulvihill/nozama-cloudsearch"
Version = "2.0.2"
Author = 'Oisin Mulvihill'
AuthorEmail = 'oisin.mulvihilli@gmail.com'
Maintainer = 'Oisin Mulvihill'
License = 'BSD'
Summary = (
    'A REST service which implements the Amazon CloudSearch for local testing '
    'purposes. This is *not* intended as a replacement for Amazon CloudSearch.'
    "See the https://github.com/oisinmulvihill/nozama-cloudsearch for more "
    "details. One handy benefit of using Nozama is it provides a way to "
    "migrate from Amazon CloudSearch to ElasticSearch."
)
Description = Summary
ShortDescription = Summary
Classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
]

with open('requirements.txt') as fd:
    needed = fd.readlines()

with open('test-requirements.txt') as fd:
    test_needed = fd.readlines()

test_suite = 'tests'

EagerResources = [
    'nozama',
]

ProjectScripts = [
]

PackageData = {
    '': ['*.*'],
}

# Web Entry points
EntryPoints = """
[paste.app_factory]
    main = nozama.cloudsearch.service:main
"""

setup(
    name=Name,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    url=ProjectUrl,
    license=License,
    classifiers=Classifiers,
    scripts=ProjectScripts,
    install_requires=needed,
    tests_require=test_needed,
    test_suite=test_suite,
    include_package_data=True,
    packages=find_packages(),
    package_data=PackageData,
    eager_resources=EagerResources,
    entry_points=EntryPoints,
)
