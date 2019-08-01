#!/bin/bash
#
# Dump All Build Outputs from Jenkins
#

if [ -z "$EMAIL" -o -z "$TOKEN" -o -z "$URL" -o -z "$JOB" -o -z "$OUT" ]; then
    echo -e "\n  Must set the following environment variables before running:"
    echo -e "\tEMAIL, TOKEN, URL, JOB, OUT\n"
    exit 1
fi

[ ! -d $OUT ] && mkdir -p $OUT
for build in $(curl -u $EMAIL:$TOKEN $URL/job/$JOB/api/json 2>/dev/null | jq -r '.builds[].number'); do
    echo Retrieving build $build
    curl -o $OUT/$build -u $EMAIL:$TOKEN $URL/job/$JOB/$build/consoleText 2>/dev/null
done
