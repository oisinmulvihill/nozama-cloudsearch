# -*- coding: utf-8 -*-
"""
A top level helper so I can call setup.py develop and it
will set up all the parts in the correct order.

See http://paver.github.com/paver for more details on it.

Oisin Mulvihill

2013-08-16T14:18:34

"""
import os
import sys
import time
import signal
import os.path
import tempfile
import subprocess

from paver import easy
from paver.path import path
from paver.options import Bunch


CWD = os.path.abspath(os.curdir)


BASKET = os.environ.get("BASKET", "")
if BASKET:
    sys.stdout.write("Using Environment BASKET '%s'." % BASKET)

SERVICEDIR = path(
    os.path.abspath(os.path.join(CWD, "nozama-cloudsearch-service"))
)

CLIENTDIR = path(
    os.path.abspath(os.path.join(CWD, "nozama-cloudsearch-client"))
)

MODELDIR = path(
    os.path.abspath(os.path.join(CWD, "nozama-cloudsearch-data"))
)


# Paver global options we'll add to:
easy.options(

    # Defaults for environment:
    develop=Bunch(
        basket=None,
        target_dir=None,
    ),

    sdist=Bunch(
        target_dir=None,
    ),

    bdist_egg=Bunch(
        target_dir=None,
    ),

    DEV_PKGS_IN_DEP_ORDER=[
        MODELDIR,
        SERVICEDIR,
        CLIENTDIR,
    ],
)


#
@easy.task
def runserver(options):
    """Run the service using the default development.ini from the service dir.
    """
    # Change in serivce directory and 'run' the pyrmaid web service:
    SERVICEDIR.chdir()
    easy.info("-- Changing to %s --" % SERVICEDIR)

    # Then switch in pkg dir to perform the set up:
    easy.info("-- Running Service --")
    pipe_output, file_name = tempfile.mkstemp()
    cmd = ["cloudsearch_service", "--config", "conf.ini"]
    p = subprocess.Popen(cmd, stdout=pipe_output, stderr=subprocess.STDOUT)
    output_fd = open(file_name)

    try:
        while not p.poll():
            # p.poll() returns None while the program is still running
            # sleep for 1 second
            time.sleep(0.01)
            line = output_fd.readline()
            if line:
                sys.stdout.write("> %s\n" % line.strip())
                sys.stdout.flush()

    except KeyboardInterrupt:
        easy.info("\tCtrl-C caught, Exitting...")
        p.send_signal(signal.SIGINT)
        time.sleep(1)
        p.kill()

    finally:
        output_fd.close()
        os.unlink(file_name)


# -- Provide a 'develop' target you'd expect in a 'normal' dist ---------------
#
#
@easy.task
@easy.cmdopts([
    ('basket=', 'i', "The cheeseshop to pull deps from."),
])
def develop(options):
    """Set up each of the profile service parts into the python environment.
    """
    global BASKET

    # Figure out and set up the runtime information:
    #
    if options.develop.basket:
        # Force '-i'
        BASKET = "-i %s" % options.develop.basket.replace("-i", "")

    # Use the python process or virtualenv python we maybe running under:
    python = sys.executable
    easy.info("Using python: <%s>" % python)

    for dev_pkg in options.DEV_PKGS_IN_DEP_ORDER:
        dev_pkg.chdir()
        easy.info("-- Changing to %s --" % dev_pkg)

        # Then switch in pkg dir to perform the set up:
        easy.info("-- Setting up %s in development mode --" % dev_pkg)

        # Set up the the package in development mode:
        easy.info("Setting up '{0}': (BASKET:'{1}') ".format(
            dev_pkg,
            BASKET
        ))
        stdout = easy.sh(
            "{python} setup.py develop {BASKET} ".format(
                python=python,
                BASKET=BASKET
            ),
            capture=True,
        )
        easy.info(stdout)


@easy.task
@easy.cmdopts([
    ('target_dir=', 't', "The directory to put build bdist_egg output."),
])
def docs(options):
    """Build the latest sphinx documentation.
    """
    docs = path(CWD) / path("docs")
    docs.chdir()
    stdout = easy.sh(
        "make html ", capture=True,
    )
    easy.info(stdout)
    m = "docs/build/html/index.html"
    easy.info("You can now open the index.html in your browser:\n\n\t%s\n" % m)

    os.chdir(CWD)
    docs_target = "nozama-cloudsearch-service/nozama/cloudsearch/service/docs/"
    html = "docs/build/html/*"
    easy.info("Copying built docs into '{0}'.".format(docs_target))
    easy.sh("cp -r {0} {1}".format(html, docs_target))


def build_it(options, target, target_dir=None):
    """Generic action handler used in other commands.
    """
    # Use the python process or virtualenv python we maybe running under:
    python = sys.executable
    easy.info("Using python: <%s>" % python)

    for dev_pkg in options.DEV_PKGS_IN_DEP_ORDER:
        target_dir_o = ""
        if target_dir:
            target_dir_o = " --dist-dir=%s " % os.path.join(
                target_dir, dev_pkg
            )

        # Change in profileservice dir (reset to here after last run):
        dev_pkg.chdir()
        easy.info("-- Changing to %s and building %s --" % (dev_pkg, target))

        stdout = easy.sh(
            "{python} setup.py {target} {target_dir} ".format(
                python=python,
                target_dir=target_dir_o,
                target=target
            ),
            capture=True,
        )
        easy.info(stdout)


@easy.task
@easy.cmdopts([
    ('target_dir=', 't', "The directory to put build bdist_egg output."),
])
def bdist_egg(options):
    """Make each of the eggs that make up the profile service project.
    """
    target_dir = None
    if options.bdist_egg.target_dir:
        target_dir = options.bdist_egg.target_dir

    build_it(options, 'bdist_egg', target_dir)


@easy.task
@easy.cmdopts([
    ('target_dir=', 't', "The directory to put build sdist output."),
])
def sdist(options):
    """Make source archive for each of the profile service project.
    """
    target_dir = None
    if options.sdist.target_dir:
        target_dir = options.sdist.target_dir

    build_it(options, 'sdist', target_dir)


@easy.task
@easy.needs('develop', 'docs')
def release(options):
    """Generated docs and apply version number changes."""


@easy.task
@easy.needs('release')
def install(options):
    """Generated docs and apply version number changes."""
