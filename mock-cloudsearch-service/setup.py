# -*- coding: utf-8 -*-
"""
Setuptools script for mock-cloudsearch-service (mock.cloudsearch.service)

"""
from setuptools import setup, find_packages

# Get the version from the source or the cached egg version:
import json
import ConfigParser
cp = ConfigParser.ConfigParser()
try:
    cp.read('../eggs_version.ini')
    version = dict(cp.items('default'))['version']
except:
    # inside and egg, read the cache version instead.
    with file("cached_version.json", "r") as fd:
        version = json.loads(fd.read())['egg_version']
else:
    # write out the version so its cached for in egg use:
    with file("cached_version.json", "w") as fd:
        fd.write(json.dumps(dict(egg_version=version)))

Name = 'mock-cloudsearch-service'
ProjectUrl = ""
Version = version
Author = ''
AuthorEmail = 'everyone at body dot co dot uk'
Maintainer = ''
Summary = 'Tornado REST Application for mock-cloudsearch-service'
License = ''
Description = Summary
ShortDescription = Summary

needed = [
    'pyramid',

    # We depend on the backend code.
    'mock-cloudsearch-common==%s' % version,
    'mock-cloudsearch-data==%s' % version,
]

test_needed = [
]

test_suite = 'mock.cloudsearch.service.tests'

EagerResources = [
    'mock',
]

ProjectScripts = [
]

PackageData = {
    '': ['*.*'],
}

# Web Entry points
EntryPoints = {
    'console_scripts': [
        'cloudsearch_service = mock.cloudsearch.service.scripts.main:main',
    ],
}

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
        "Framework :: Tornado",
        "Topic :: Internet :: WWW/HTTP",
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
    namespace_packages=['mock', 'mock.cloudsearch'],
)
