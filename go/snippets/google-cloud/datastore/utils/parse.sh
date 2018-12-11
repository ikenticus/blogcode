# cat full_sports | sed 's/^ *[0-9]*//' | grep -v : |  sort -u > list1

cat list1 | while read line; do
    IFS=_
    set -- $line
    unset IFS
    if [ -z "${line##player*}" ]; then
        echo $line | cut -d_ -f1-4
    else
        echo $line | cut -d_ -f1-3
    fi
done | tee list2

cat list2 | sort -u > list3
