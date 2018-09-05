read T

: '
# Times out for Testcase(s) 7-9
i=0
while [ $i -lt $T ]; do
    read S
    j=0
    odd=()
    even=()
    while [ $j -lt ${#S} ]; do
        if [ $[j%2] -eq 1 ]; then
            odd+=(${S:j:1})
        else
            even+=(${S:j:1})
        fi
        let j=j+1 
    done
    printf "%s" ${even[@]} " " ${odd[@]} $'\n'
    let i=i+1 
done
'

# https://stackoverflow.com/questions/10586153/split-string-into-an-array-in-bash
# https://stackoverflow.com/questions/7578930/bash-split-string-into-character-array
# https://stackoverflow.com/questions/1951506/add-a-new-element-to-an-array-without-specifying-the-index-in-bash
# https://stackoverflow.com/questions/1527049/join-elements-of-an-array
# https://stackoverflow.com/questions/43158140/way-to-create-multiline-comments-in-bash

: '
# Still times out for Testcase(s) 7-9
parse() {
    local n=$1
    local S=$2
    j=0
    while [ $j -lt ${#S} ]; do
        [ $[j%2] -eq $n ] && echo -n ${S:j:1}
        let j=j+1 
    done
}
i=0
while [ $i -lt $T ]; do
    read S
    parse 0 $S
    echo -n " "
    parse 1 $S
    echo
    let i=i+1 
done
'

# Still times out for Testcase(s) 7-9
for ((i = 0; i < T ; i++)); do
    read S
    unset even odd
    for ((j = 0; j < ${#S}; j++)); do
        if [ $((j%2)) -eq 0 ]; then
            even="$even${S:j:1}"
        else
            odd="$odd${S:j:1}"
        fi
    done
    echo "$even $odd"
done
