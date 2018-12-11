for line in $(cat list3); do
    IFS=_
    set -- $line
    unset IFS
    type=$(echo $1 | sed 's/image/Image/; s/split/Split/; s/stat/Stat/;')
    dtype=$(echo $1 | sed 's/image/-image/; s/split/-split/; s/stat/-stat/;')
    if [ -z "${dtype%%*-images}" ]; then
        ftype=$dtype
    else
        ftype=$(echo $dtype | sed 's/-/_/g')
    fi
    league=$(echo $2 | tr [a-z] [A-Z])
    season=$3
    case $league in
        MLB) sport=baseball ;;
        MLS) sport=soccer ;;
        NHL) sport=hockey ;;
        NFL|NCAAF) sport=football ;;
        *) sport=basketball ;;
    esac
    if [ $# -gt 3 ]; then
        file=${ftype}_$4_${league}
    else
        file=${ftype}_${league}
    fi
    url="http://localhost:8080/input?Sport=$sport&League=$league&DataType=$dtype&Season=$season"
    url="$url&FeedURL=http://xml.sportsdirectinc.com/sport/v2/$sport/$league/$dtype/$season/$file.xml"
    url="$url?apiKey=EF9ADB80-0E0F-40D3-973F-1E89BB5335D8"
    echo URL: $url
    curl $url
    sleep 300
done


