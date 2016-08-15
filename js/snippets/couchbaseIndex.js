/*
    Functions to create/check/drop Couchbase indexes
*/

var bucketName = 'bucket';
var password = 'password';
var couchbase = require('couchbase')
var N1qlQuery = couchbase.N1qlQuery;
var cluster = new couchbase.Cluster('couchbase://hostname/');
var bucket = cluster.openBucket(bucketName, password);
    //bucket.operationTimeout = 1000 * 300;
    //bucket.connectionTimeout = 1000 * 300;
var format = require('string-format');

var createPrimaryIndex = function() {
    bucket.query(
        N1qlQuery.fromString(format('CREATE PRIMARY INDEX ON {}', bucketName)),
        function (err, rows) {
            console.log(rows);
            process.exit();
        }
    );
}

var createIndex = function(indexName, indexKeys) {
    if (indexKeys == null) indexKeys = indexName;
    bucket.query(
        N1qlQuery.fromString(format('CREATE INDEX {} ON {}({})', indexName, bucketName, indexKeys)),
        function (err, rows) {
            console.log(rows);
            process.exit();
        }
    );
}

var displayIndex = function(indexName) {
    bucket.query(
        N1qlQuery.fromString(format('SELECT * FROM system:indexes WHERE name="{}"', indexName)),
        function (err, rows) {
            console.log(rows);
            process.exit();
        }
    );
}

var dropIndex = function(indexName) {
    bucket.query(
        N1qlQuery.fromString(format('DROP INDEX {}.{}', bucketName, indexName)),
        function (err, rows) {
            console.log(rows);
            process.exit();
        }
    );
}

// MAIN
switch(process.argv[2]) {
    case 'drop':
        dropIndex(process.argv[3]);
        break;
    case 'create':
        createIndex(process.argv[3], process.argv[4]);
        break;
    case 'display':
        displayIndex(process.argv[3]);
        break;
}

