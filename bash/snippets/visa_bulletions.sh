#!/bin/bash
#
# Retrieve cutoff dates for F4 visa
#

TMP=/tmp/visa

scrape_visa() { # circa 2023
    [ ! -d $TMP ] && mkdir $TMP
    SITE=https://travel.state.gov
    MAIN=/content/travel/en/legal/visa-law0/visa-bulletin.html
    pushd $TMP

    echo "Retrieving index"
    [ ! -f index.html ] && \
    curl -so index.html ${SITE}${MAIN}

    [ ! -d output ] && mkdir output
    echo -n "Retrieving each bulletin index "
    for page in $(egrep -i "Bulletin for" index.html | sed 's/^.*href="//; s/".*$//' | grep -v title); do
        # echo -e "\nProcessing $page ($?)"
        
        [ ! -f ${page##*/} ] && curl -sO ${SITE}/$page
        pdf=$(grep 'pdf"' ${page##*/} | sed 's/^.*href="//; s/".*$//' | egrep -v "target|Statistics")
        if [ $? -gt 0 ]; then
            echo -n h
            # echo "Verify: $page ($?)"

            cutoff=$(egrep -A2 '>(F4|4th|4<sup>th|4rd)<' ${page##*/} | grep -v '^</t.>$' | head -2 | tail -1 | sed 's/&nbsp;//; s/<[^>]*>//g;')
            echo -n .
            # echo "Verify: $cutoff ($?)"
            
            ugly=$(echo ${page##*/} | awk -F- '{print $(NF-1)$NF}' | cut -d. -f1)
            stamp=$(date -j -v-1d -f "%B%Y" "$ugly" +%b-%Y)
            # echo "Verify: $stamp ($?) $ugly $page"

            xml=$(grep -B1 Volume ${page##*/} | head -2)
            title=$(echo $(echo $xml) | sed 's/&nbsp;/ /g; s/<[^>]*>//g;')
            clean=$(date -j -v-1d -f "%B%Y" "$ugly" +output/visa-bulletin-%Y-%m.html)
            [ ! -f $clean ] && cp ${page##*/} $clean
        else
            echo -n p
            # echo "Verify: $pdf ($?)"

            [ ! -f ${pdf##*/} ] && curl -sO ${SITE}/$pdf
            # brew install xpdf
            txt=${pdf%.pdf}.txt
            txt=${txt##*/}
            echo -n :
            # echo "Verify: $txt ($?)"

            [ ! -f $txt ] && pdftotext ${pdf##*/} $txt
            cutoff=$(grep -A2 ^F4$ $txt | tail -1 | cut -c-7)
            [ -z "$cutoff" ] && cutoff=$(grep -A7 F4$ $txt | grep -v ^$ | tail -1 | cut -c-7)
            [ -z "$cutoff" ] && cutoff=$(grep ^F4 $txt | tail -1 | cut -c4-10)
            echo -n .
            # echo "Verify: $cutoff ($?)"

            ugly=$(echo $pdf | sed 's/.pdf$//; s/^.*tin[_-]*//; s/%20//g; s/_//g;')
            stamp=$(date -j -v-1d -f "%B%Y" "$ugly" +%b-%Y)
            # echo "Verify: $stamp ($?)"

            title=$(grep Volume $txt | head -1)
            clean=$(date -j -v-1d -f "%B%Y" "$ugly" +output/visa-bulletin-%Y-%m.pdf)
            [ ! -f $clean ] && cp ${pdf##*/} $clean
        fi 
        echo -e "$stamp\t$cutoff\t\t$title" >> output/f4-hk-visa-cutoffs.txt
        [ -z "${stamp##Jan*}" ] && echo >> output/f4-hk-visa-cutoffs.txt
    done
    echo " --- Done!"
    popd
}

get_html() { # circa 2019
    for m in $(seq 144); do
        MONYR=$(date -v-${m}m +%b-%y)
        monyr=$(echo $MONYR | tr [A-Z] [a-z])
        #curl https://www.uscis.gov/visabulletin-$monyr -o ${TMP}-$monyr 2> /dev/null

        MONTHYEAR=$(date -v-${m}m +%B-%Y)
        monthyear=$(echo $MONTHYEAR | tr [A-Z] [a-z])
        curl https://www.uscis.gov/green-card/green-card-processes-and-procedures/visa-availability-priority-dates/when-file-your-adjustment-status-application-family-sponsored-or-employment-based-preference-visas-$monthyear -o ${TMP}-$monyr 2> /dev/null

        PRIOR=$(cat ${TMP}-$monyr | grep -A2 F4 | sed -ne 's/^.*\([0-9][0-9][A-Z][A-Z][A-Z][0-9][0-9]\).*$/\1/p')
        echo -e "$MONYR\t$(echo $PRIOR | sed 's! ! / !')"
    done | tee -a visabulletin.txt
    unix2dos visabulletin.txt
}

get_pdf() { # OG
    for m in $(seq 144); do
        MONTHYEAR=$(date -v-${m}m +%B%Y)
        yearmo=$(date -v-${m}m +%Y%m)
        curl https://travel.state.gov/content/dam/visas/Bulletins/visabulletin_$MONTHYEAR.pdf -o visabulletin_$yearmo.pdf
    done
}

###  MAIN
# get_pdf
# get_html
scrape_visa
