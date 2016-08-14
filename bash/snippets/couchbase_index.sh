#!/bin/bash
#
#   Functions to create/check/drop Couchbase indexes
#

PORT=8093
HOST=hostname

BUCKET=bucket
USER=username
PASS=password

create_primary() {
    curl -v http://$HOST:$PORT/query/service \
         -d "statement=CREATE PRIMARY INDEX ON ${BUCKET}&creds=[{\"user\":\"local:$USER\", \"pass\":\"$PASS\"}];"
}

create_index() {
    indexName=$1
    indexKeys=${2:-$1}
    curl -v http://$HOST:$PORT/query/service \
         -d "statement=CREATE INDEX ${indexName} ON ${BUCKET}(${indexKeys})&creds=[{\"user\":\"local:$USER\", \"pass\":\"$PASS\"}];"
}

select_index() {
    indexName=$1
    curl -v http://$HOST:$PORT/query/service \
         -d "statement=SELECT * FROM system:indexes WHERE name=\"${indexName}\"&creds=[{\"user\":\"local:$USER\", \"pass\":\"$PASS\"}];"
}

drop_index() {
    indexName=$1
    curl -v http://$HOST:$PORT/query/service \
         -d "statement=DROP INDEX ${BUCKET}.${indexName}&creds=[{\"user\":\"local:$USER\", \"pass\":\"$PASS\"}];"
         #-d "statement=DROP INDEX `${BUCKET}`.`${indexName}`&creds=[{\"user\":\"local:$USER\", \"pass\":\"$PASS\"}];"
}

##########  MAIN  ##########
action=$1
shift
case $action in
    create) create_index $@;;
    select) select_index $@;;
    drop)   drop_index $@;;
esac

