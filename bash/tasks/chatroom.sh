#!/bin/bash
#
#   Task: Chatroom
#

usage() {
    echo -e "Display chatroom statistics\nUsage: ${0##*/} <chatfile> <n>"
}

parse() {
    # bash does not support associative arrays before v4
    # we could use env variables, but lets just use tmpFiles
    rm -f /tmp/stat_*    # explicitly w/o var to avoid 911
    TMP=/tmp/stat

    local data=("$@")
    for c in "${data[@]}"; do
        if [ ! -z "$c" ]; then
            user=${c%%:*}
            chat=${c#*:}
            chat=${chat## }
            echo $chat >> ${TMP}_$user
        fi
    done

    for s in ${TMP}_*; do
        wc -w $s | sed 's!'${TMP}'_!!'
    done | sort -rn > ${TMP}OUT
}

output() {
    local order=$1
    rank=${order##-}
    if [ $order == $rank ]; then
        most=1
        mostWord=most
    else
        mostWord=least
    fi

    if [ $rank -eq 0 ]; then
        printf 'List of %s wordy users:\n' $mostWord
        #[ -z "$most" ] && tac ${TMP}OUT || cat ${TMP}OUT
        # when tac does not exist
        if [ -z "$most" ]; then
            cat ${TMP}OUT | sort -n
        else
            cat ${TMP}OUT
        fi
    else
        if [ -z "$most" ]; then
            stat=$(cat ${TMP}OUT | tail -$rank | head -1)
        else
            stat=$(cat ${TMP}OUT | head -$rank | tail -1)
        fi
        set -- $stat
        count=$1
        user=$2
        printf 'The %s %s wordy user is (%s) with %d words\n' $rank $mostWord $user $count
    fi
}

# main
if [ $# -lt 2 ]; then
    usage
    exit 1
fi
chatfile=$1
IFS=$'\n' read -d '' -r -a data < $chatfile
parse "${data[@]}"
output $2
