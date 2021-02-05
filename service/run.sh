#!/bin/bash

# avoid error message on ctrl-c
cleanup() {
    echo
    exit 0
}
trap cleanup EXIT

# get the directory containing this script
SCRIPT_DIR=`dirname $0`

# enter directory containing this script
cd ${SCRIPT_DIR}

# run the timeseris service and discard output to terminal
echo
echo "--------------------------------------------------------------------------"
echo "The Timeseries Service is now running in the REPRO."
echo "Terminal output from the service is directed to service/log.txt."
echo
echo "Terminate the service by typing CTRL-C in this terminal."
echo "--------------------------------------------------------------------------"
${JAVA_HOME}/bin/java                                       \
    -Dspring.config.location=application.properties         \
    -jar ${REPRO_MNT}/service/timeseries-service-0.2.1.jar  \
    &> ${REPRO_MNT}/service/log.txt
