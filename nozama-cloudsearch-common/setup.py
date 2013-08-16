# -*- coding: utf-8 -*-
"""
Setuptools script for nozama-cloudsearch-common (nozama.cloudsearch.common)

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

Name = 'nozama-cloudsearch-common'
ProjectUrl = ""
Version = version
Author = ''
AuthorEmail = 'everyone at body dot co dot uk'
Maintainer = ''
Summary = ' nozama-cloudsearch-common '
License = ''
Description = Summary
ShortDescription = Summary

needed = [
]

test_needed = [
]

test_suite = 'nozama.cloudsearch.common.tests'

EagerResources = [
    'nozama',
]

# Example including shell script out of scripts dir
ProjectScripts = [
    #'nozama.cloudsearch.common/scripts/somescript',
]

PackageData = {
    '': ['*.*'],
}

# Example console script and paster template integration:
EntryPoints = {
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
