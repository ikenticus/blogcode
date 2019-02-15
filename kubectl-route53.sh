#!/bin/bash
#
#   Check and update DNS to match kubectl get svc
#

[ -z "$SERVICE" ] && SERVICE=kube-svc
[ -z "$DNSNAME" ] && DNSNAME=www.example.com

usage() {
    echo -e "\nUsage: ${0##*/} <kubectl-svc> <dns-name>\n\n  i.e. ${0##*/} $SERVICE $DNSNAME\n"
    exit 0
}

get_service_dns() {
    TARGET=$(kubectl get svc $SERVICE -o json | jq -r '.status.loadBalancer.ingress[0].hostname')
    if [ -z "$TARGET" ]; then
        # try across all namespaces
        TARGET=$(kubectl get svc --all-namespaces -o json | jq -r ".items[] | select(.metadata.name == \"$SERVICE\") | .status.loadBalancer.ingress[0].hostname")
    fi
}

cleanup_dns() {
    FQDN=${DNSNAME%.}.
    IFS=.
        set -- ${DNSNAME%.}
    unset IFS
    CNT=$#; TLD=${!CNT}
    CNT=$[CNT-1]; SUB=${!CNT}
    DOMAIN=$SUB.$TLD.
}

get_hosted_zone() {
    HOSTZONE=$(aws route53 list-hosted-zones | jq -r ".HostedZones[] | select(.Name == \"$DOMAIN\") | .Id")
    if [ -z "$HOSTZONE" ]; then
        echo "ERROR: No hosted-zone-id found for $DOMAIN under your control, exiting"
        exit 1
    fi
}

get_current_record() {
    CURRENT=$(aws route53 list-resource-record-sets --hosted-zone-id $HOSTZONE | jq -r ".ResourceRecordSets[] | select (.Name == \"$FQDN\") | .AliasTarget.DNSName")
    if [ "$CURRENT" == "$TARGET." ]; then
        echo "No changes necessary, $SERVICE already set to $TARGET"
        exit 0
    fi
}

get_aws_hostzone() {
    # https://docs.aws.amazon.com/general/latest/gr/rande.html#elb_region
    local awsdns=$1
    case $awsdns in
        *.us-east-1.*) echo Z35SXDOTRQ7X7K ;;
        *.us-east-2.*) echo Z3AADJGX6KTTL2 ;;
        *.us-west-1.*) echo Z368ELLRRE2KJ0 ;;
        *.us-west-2.*) echo Z1H1FL5HABSF5 ;;
    esac
}

route53_change() {
    local ACTION=$1
    local AWSDNS=$2
    local AWSHZI=$(get_aws_hostzone $AWSDNS)
    cat >> $TMP << EOF
        {
            "Action": "$ACTION",
            "ResourceRecordSet": {
                "Name": "$FQDN",
                "Type": "A",
                "AliasTarget": {
                    "HostedZoneId": "$AWSHZI",
                    "DNSName": "$AWSDNS",
                    "EvaluateTargetHealth": false
                }
            }
        }
EOF
}

update_dns() {
    cat > $TMP << EOF
{
    "Comment": "Deleting/Creating A record for $DNSNAME",
    "Changes": [
EOF
    if [ ! -z "$CURRENT" ]; then
        route53_change DELETE $CURRENT
        echo , >> $TMP
    fi
    route53_change CREATE $TARGET.
    echo -e "    ]\n}" >> $TMP

    CHANGE=$(aws route53 change-resource-record-sets --hosted-zone-id $HOSTZONE --change-batch file://$TMP)
    CHANGEID=$(echo $CHANGE | jq -r '.ChangeInfo.Id')
    echo "$CHANGE"
    echo Monitor change using: aws route53 get-change --id $CHANGEID
}


### MAIN
[ "${1#--}" == "help" -o "$1" == "-h" ] && usage
[ $# -ge 1 ] && SERVICE=$1
[ $# -ge 2 ] && DNSNAME=$2
TMP=/tmp/$DNSNAME

get_service_dns
cleanup_dns
get_hosted_zone
get_current_record
update_dns
