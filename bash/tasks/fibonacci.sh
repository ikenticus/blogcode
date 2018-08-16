#!/bin/bash
#
#   Task: Fibonacci
#

usage() {
    echo -e "Calculate the Nth Fibonacci number\nUsage: ${0##*/} <n>"
}

SEQ=(0 1)
if [ $# -eq 0 ]; then
    usage
    exit 1
elif [ $1 -le 1 ]; then
    echo "F($1) = $1"
    if [ $1 -lt 1 ]; then
        unset SEQ[1]
    fi
else
    NUM=$1
    if [ $NUM -gt 1 ]; then
        for ((i=1; i<$NUM; i++)); do
            idx=${#SEQ[@]}
            SEQ[$idx]=$[${SEQ[$[idx-1]]}+${SEQ[$[idx-2]]}]
        done
    fi
    SIZE=${#SEQ[@]}
    echo "F($NUM) = ${SEQ[$[SIZE-1]]}"
fi
echo "Sequence: ${SEQ[*]}"
