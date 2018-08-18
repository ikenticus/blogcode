#!/bin/bash
#
#   Task: Analog Clock
#

usage() {
    echo -e "Calculate the angle betwwen hour and minute hands\nUsage: ${0##*/} <HH:MM>"
}

degree() {
    local num=$1
    local min=$2
    if [ -z "$min" ]; then
        echo $[num*6]
    else # hour hand
        num=$[num%12]
        num=$[num*30]
        num=$[num+(min/12)]
        if [ $num -lt $min ]; then
            echo $[num+360]
        else
            echo $num
        fi
    fi
}

# main
if [ $# -lt 1 ]; then
    usage
    exit 1
fi
IFS=':'
set -- $1
unset IFS
min=$(degree $2)
hour=$(degree $1 $min)
echo $[hour-min] degrees
