#!/bin/bash
#
# This is the jenkins hookup to run the tests in a clean
# environment. I expect python-setuptools and python-virtualenv
# packages to be installed on the system.
#
VIRTUALENV=${VIRTUALENV:=virtualenv}
TMPBUILDDIR=${TMPBUILDDIR:=/tmp/p_`python -c "import uuid;print(str(uuid.uuid4()).replace('-',''))"`}
export CHECKOUT_ROOT=`pwd`
#CHEESESHOP_DIR=${CHEESESHOP_DIR:=/var/www/cheeseshop/httpdocs}
#export BASKET=${BASKET:="-i http://"}


function setup() {
    rm -rf ${TMPBUILDDIR}

    # Create a clean environment without anything install fresh for testing:
    $VIRTUALENV --clear --no-site-packages ${TMPBUILDDIR}
    source  ${TMPBUILDDIR}/bin/activate
    if [ "$?" == 1 ];
    then
        echo "Error setting up virtual environment for tests!"
        return 1
    fi

    # Install testing dependancies:
    #for dep in nose NoseXUnit sphinx; do
    for dep in nose pytest sphinx; do
        $TMPBUILDDIR/bin/easy_install ${BASKET} $dep
        if [ "$?" == 1 ];
        then
            echo "Error installing $dep!"
            return 1
        fi
    done

    # Manual set up of each of the package using out Egg cache:
    #
    # This uses the special pavement.py to correctly set up
    # all profile service parts already.
    #
    $TMPBUILDDIR/bin/python setup.py develop ${BASKET} ;
    if [ "$?" == 1 ];
    then
        echo "Error setting up package for test run!"
        return 1
    fi

    return 0
}


function run_tests() {
    # Run the tests:
    #$TMPBUILDDIR/bin/python setup.py nosetests -sv
    $TMPBUILDDIR/bin/py.test -sv pp
    # --with-nosexunit
    if [ "$?" == 1 ];
    then
        echo "Error tests FAILED to run!"
        return 1
    fi
}

function build_dist() {
    # Build the egg and source dist:
    $TMPBUILDDIR/bin/python setup.py bdist_egg sdist
    if [ "$?" == 1 ];
    then
        echo "Error source and egg dist generation FAILED!"
        return 1
    fi

    # Run nose tests with the top-level nose config file.
    cd $CHECKOUT_ROOT/docs
    make html
    if [ "$?" == 1 ];
    then
        echo "Error generating documentation FAILED!"
        return 1
    fi
}


function pypi_publish() {
    # Move the eggs and sdist to our pypi on our own
    # cheeseshop.imagination-services.com
    #
    # I'll only do this step we are on the machine with cheeseshop:
    if [ -d "$CHEESESHOP_DIR" ];
    then
        # Recover just the egg name:
        NAME=`cat *.egg-info/PKG-INFO | grep 'Name:' | sed -e "s/Name:.//"`
        if [ -n "$NAME" ];
        then
            # Make the top level name in pypi dir then put the eggs/sdist
            # into this location. This is needed to maintain compatibility
            # and so easy_install -i <my pypi> NAME will work.
            #
            echo "Package name: '$NAME'."
            mkdir -p $CHEESESHOP_DIR/$NAME
            cp dist/* $CHEESESHOP_DIR/$NAME/
            echo "$CHEESESHOP_DIR/$NAME: "`ls $CHEESESHOP_DIR/$NAME`
        else
            echo "unable to determine Python Package Name!"
            return 1
        fi
    fi

    return 0
}


function tear_down() {
    # clean up:
    rm -rf $TMPBUILDDIR
}


function print_stage() {
    # Make it easier to see which stage stdout output belongs to.
    echo
    echo "---------------------------------------------------------------------"
    echo
    echo $1
    echo
    echo "---------------------------------------------------------------------"
    echo
}

function main() {
    # Don't continue a step in fails.
    print_stage "Set Up Environment."
    setup
    if [ "$?" == 1 ];
    then
        return 1
    fi

    print_stage  "Run Tests."
    run_tests
    if [ "$?" == 1 ];
    then
        return 1
    fi

    print_stage "Build Release."
    build_dist
    if [ "$?" == 1 ];
    then
        return 1
    fi

#    print_stage "Publish to Internal Cheeseshop."
#    pypi_publish
#    if [ "$?" == 1 ];
#    then
#        return 1
#    fi

    print_stage "Tear Down Clean Up."
    tear_down
}

main
