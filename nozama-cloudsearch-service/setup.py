# -*- coding: utf-8 -*-
"""
Setuptools script for nozama-cloudsearch-service (nozama.cloudsearch.service)

"""
from setuptools import setup, find_packages

Name = 'nozama-cloudsearch-service'
ProjectUrl = ""
Version = "1.0.0dev"
Author = ''
AuthorEmail = 'everyone at pythonpro dot co dot uk'
Maintainer = ''
Summary = 'Pyramid REST Application for nozama-cloudsearch-service'
License = ''
Description = Summary
ShortDescription = Summary

needed = [
    # for docs generationself.
    'sphinx',
]

test_needed = [
]

test_suite = 'nozama.cloudsearch.service.tests'

EagerResources = [
    'nozama',
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
