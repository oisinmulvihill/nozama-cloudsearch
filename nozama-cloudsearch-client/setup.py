# -*- coding: utf-8 -*-
"""
Setuptools script for nozama-cloudsearch-client (nozama.cloudsearch.client)

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

Name = 'nozama-cloudsearch-client'
ProjectUrl = "https://github.com/oisinmulvihill/nozama-cloudsearch"
Version = version
Author = 'Oisin Mulvihill'
AuthorEmail = 'oisin dot mulvihill a-t  gmail dot com'
Maintainer = 'Oisin Mulvihill'
Summary = (
    "The Python REST client library to talk to the nozama-cloudsearch service."
    "The implements the Amazon CloudSearch and Nozama's testing helper API."
    "See the http://nozama-cloudsearch.readthedocs.org/en/latest/ for more "
    "details."
)
License = 'BSD'
Description = Summary
ShortDescription = Summary

needed = [
    'requests',
    'cmdln',
]

test_needed = [
    'evasion-common',
]

test_suite = 'nozama.cloudsearch.client.tests'

EagerResources = [
    'nozama',
]

ProjectScripts = [
]

PackageData = {
    '': ['*.*'],
}

EntryPoints = {
    'console_scripts': [
        'cloudsearch-admin = nozama.cloudsearch.client.admintool:main',
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
    ],
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
    namespace_packages=['nozama', 'nozama.cloudsearch'],
)
