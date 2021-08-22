import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fd:
    needed = fd.readlines()

with open('test-requirements.txt') as fd:
    test_needed = fd.readlines()

setuptools.setup(
    name="nozama-cloudsearch",
    version="2.0.4",
    author="Oisin Mulvihill",
    author_email="oisin.mulvihilli@gmail.com",
    description="""
    A REST service which emulates Amazon CloudSearch for local testing.
    """.strip(),
    license="BSD",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/oisinmulvihill/nozama-cloudsearch",
    packages=setuptools.find_packages(),
    entry_points="""
    [paste.app_factory]
        main = nozama.cloudsearch.service:main
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=needed,
    tests_require=test_needed,
    test_suite="tests",
)
