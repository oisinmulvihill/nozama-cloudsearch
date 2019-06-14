# -*- coding: utf-8 -*-
"""
Setuptools script for content-classify-service (content.classify.service)

"""
from setuptools import setup, find_packages

# Get the version from the source or the cached egg version:
version = "2.0.0"
Name = 'nozama-cloudsearch'
ProjectUrl = "https://github.com/oisinmulvihill/nozama-cloudsearch"
Version = version
Author = 'Oisin Mulvihill'
AuthorEmail = 'oisin dot mulvihill a-t  gmail dot com'
Maintainer = 'Oisin Mulvihill'
License = 'BSD'
Summary = (
    'A REST service which implements the Amazon CloudSearch for local testing '
    'purposes. This is *not* intended as a replacement for Amazon CloudSearch.'
    "See the http://nozama-cloudsearch.readthedocs.org/en/latest/ for more "
    "details. One handy benefit of using Nozama is it provides a way to "
    "migrate from Amazon CloudSearch to ElasticSearch."
)
Description = Summary
ShortDescription = Summary

with open('requirements.txt') as fd:
    needed = fd.readlines()

with open('test-requirements.txt') as fd:
    test_needed = fd.readlines()

test_suite = 'nozama.cloudsearch.service.tests'

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
    url=ProjectUrl,
    name=Name,
    zip_safe=False,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    keywords='web wsgi bfg pylons pyramid',
    license=License,
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
