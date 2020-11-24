#!/bin/bash

# avoid error message on ctrl-c
cleanup() {
    echo
    exit 0
}
trap cleanup EXIT

# run the yw-editor-web service and discard output to terminal
${JAVA_HOME}/bin/java                                       \
    -Dspring.config.location=application.properties         \
    -jar ${REPRO_MNT}/service/timeseries-service-0.2.1.jar  \
    &> ${REPRO_MNT}/service/logs/log.txt
