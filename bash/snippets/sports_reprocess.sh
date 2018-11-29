#!/bin/bash
#
# Grab teams/results and re-process designated type
#

SELF=${0##*/}

if [ $# -lt 3 ]; then
    echo "Usage: $SELF sport subsport season base [type] [env]"
    exit 0
fi

sport=$1
subsport=$2
season=$3
base=$4
case $base in
    results)
        type=${5:-player-stats}
        key=competition
        ;;
    teams)
        type=${5:-season-stats}
        key=team
        ;;
esac

if [ -z $type ]; then
    echo "Aborting, invalid base specified: $base"
fi

[ $# -gt 5 ] && host=https://sports-aggregator.$6.gannettdigital.com
[ -z $host ] && host=http://localhost:3000

echo Scanning for $type from $sport/$subsport $season $base on $host

temp=/tmp/$type
curl ${host}/feed/process/sdi_${sport}_${subsport}_${base}_${season} 2> /dev/null | sed 's/"/\
/g' | grep "/$key:" | cut -d: -f2 | gtac | while read each; do
    echo Reprocessing $type for $season $key $each on $host
    if [ "$base" == "results" ]; then
        curl -o $temp ${host}/feed/process/sdi_${sport}_${subsport}_${type}_${each} 2> /dev/null
    else
        curl -o $temp ${host}/feed/process/sdi_${sport}_${subsport}_${type}_${each}_${season} 2> /dev/null
    fi
    sleep ${DELAY:-5}
done

