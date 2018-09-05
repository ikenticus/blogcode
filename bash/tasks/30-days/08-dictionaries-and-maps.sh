read n

declare -A entry
for ((i = 0; i < n; i++)); do
    read e
    # Associative arrays only exist in BASH 4+
    #entry["${e%% *}"] = ${e##* } 
done

# need to figure out how to read until no more
while read q; do
    if [ -z ${entry[$q]} ]; then
        echo 'Not found'
    else
        echo $q=${entry[$q]}
    fi
done

