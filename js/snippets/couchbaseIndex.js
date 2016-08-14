/*
    Functions to create/check/drop Couchbase indexes
    (not working yet...)
*/

var bucketName = 'bucket';
var password = 'password';
var couchbase = require('couchbase')
var cluster = new couchbase.Cluster('couchbase://hostname/');
var bucket = cluster.openBucket(bucketName, password);
var N1qlQuery = couchbase.N1qlQuery;

var createPrimaryIndex = function() {
    bucket.query(
        N1qlQuery.fromString('CREATE PRIMARY INDEX ON $1'),
        [bucketName],
        function (err, rows) {
            console.log(rows);
        }
    );
}

var createIndex = function(indexName, indexKeys) {
    if (indexKeys == null) indexKeys = indexName;
    bucket.query(
        N1qlQuery.fromString('CREATE INDEX $1 ON $2($3)'),
        [indexName, bucketName, indexKeys],
        function (err, rows) {
            console.log(rows);
        }
    );
}

var selectIndex = function(indexName) {
    bucket.query(
        N1qlQuery.fromString('SELECT * FROM system:indexes WHERE name="$1"'),
        [indexName],
        function (err, rows) {
            console.log(rows);
        }
    );
}

var dropIndex = function(indexName) {
    bucket.query(
        N1qlQuery.fromString('DROP INDEX $1.$2'),
        [bucketName, indexName],
        function (err, rows) {
            console.log(rows);
        }
    );
}

// MAIN
switch(process.argv[2]) {
    case 'create':
        createIndex(process.argv[3], process.argv[4]);
        break;
    case 'select':
        selectIndex(process.argv[3]);
        break;
    case 'drop':
        dropIndex(process.argv[3]);
        break;
}

