#!/bin/bash
#
#   Update SG permissions with EKS nodes
#

[ -z "$CLUSTER" ] && CLUSTER=test-worker
[ -z "$SECGRP" ] && SECGRP=security-group
[ -z "$REGION" ] && REGION=us-east-1
[ -z "$PORT" ] && PORT=22

usage() {
    echo -e "\nUsage: ${0##*/} <cluster> <secgrp> <region> <port>\n\n  i.e. ${0##*/} $CLUSTER $SECGRP $REGION $PORT\n"
    exit 0
}

get_eks_nodegroup() {
    NODEGROUP=$(eksctl get nodegroup --cluster $CLUSTER -r $REGION -o json)
    if [ $? -gt 0 ]; then
        echo ERROR: $NODEGROUP
        exit 1
    else
        NODEGROUP=$(echo $NODEGROUP | jq -r '.[].Name')
    fi
}

get_nodegroup_ips() {
    ZONES=$(aws ec2 describe-instances --region $REGION --filters Name=network-interface.group-name,Values=eksctl-$CLUSTER-nodegroup-$NODEGROUP-* \
        --query 'Reservations[].Instances[].[Placement.AvailabilityZone,PublicIpAddress]' --output text | sort | perl -pe 's/\t+/=/g')
}

get_sg_ingress() {
    INGRESS=$(aws ec2 describe-security-groups --group-name $SECGRP --region $REGION | jq -r ".SecurityGroups[].IpPermissions[].IpRanges[] | select(.Description | startswith(\"EKS $CLUSTER\")) | \"\(.Description)=\(.CidrIp)\"" | perl -pe 's#^.+\s(\S+)/\d+$#\1#' | sort)
}

revoke_sg_ingress() {
    if [ -z "$INGRESS" ]; then
        echo "No SG ingress security groups to revoke related to EKS $CLUSTER!"
        return
    fi
    echo -e "Revoking current SG ingress security groups:\n$INGRESS"
    RULES=$(echo $INGRESS | sed 's/=/,CidrIp=/g' | sed "s# #/32},{Description=EKS $CLUSTER #g")
    IPPERMS="IpProtocol=tcp,FromPort=$PORT,ToPort=$PORT,IpRanges=[{Description=EKS $CLUSTER $RULES/32}]"
    #echo aws ec2 revoke-security-group-ingress --region $REGION --group-name $SECGRP --ip-permissions "$IPPERMS"
    aws ec2 revoke-security-group-ingress --region $REGION --group-name $SECGRP --ip-permissions "$IPPERMS"
}

authorize_sg_ingress() {
    echo -e "Authorizing latest EKS zones into SG ingress:\n$ZONES"
    RULES=$(echo $ZONES | sed 's/=/,CidrIp=/g' | sed "s# #/32},{Description=EKS $CLUSTER #g")
    IPPERMS="IpProtocol=tcp,FromPort=$PORT,ToPort=$PORT,IpRanges=[{Description=EKS $CLUSTER $RULES/32}]"
    #echo aws ec2 authorize-security-group-ingress --region $REGION --group-name $SECGRP --ip-permissions "$IPPERMS"
    aws ec2 authorize-security-group-ingress --region $REGION --group-name $SECGRP --ip-permissions "$IPPERMS"
}

update_sg_ingress() {
    if [ "$ZONES" == "$INGRESS" ]; then
        echo -e "SG ingress rules already match EKS zones:\n$ZONES"
        exit 0
    else
        revoke_sg_ingress
        authorize_sg_ingress
    fi
}


### MAIN
[ "${1#--}" == "help" -o "$1" == "-h" ] && usage
[ $# -ge 1 ] && CLUSTER=$1
[ $# -ge 2 ] && SECGRP=$2
[ $# -ge 3 ] && REGION=$3
[ $# -ge 4 ] && REGION=$4

get_eks_nodegroup
get_nodegroup_ips
get_sg_ingress
update_sg_ingress
