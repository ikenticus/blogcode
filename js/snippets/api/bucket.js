'use strict';

var couchbase = require('couchbase');
var format = require('string-format');

var logger = require('../logger.js')();

module.exports = function(datastore) {
    // if scalr variable defined, overwrite ['localhost']
    if (process.env[datastore.scalr] !== undefined) {
        if (datastore.hosts.length === 1) {
            datastore.hosts = process.env[datastore.scalr].replace(/[\[\]\ \']/g, '').split(',');
        }
    }
    logger.info('Couchbase cluster:', datastore.hosts);
    var cluster = new couchbase.Cluster(datastore.hosts);
    var bucket = cluster.openBucket(datastore.container, datastore.password, function() {
        if (bucket.connected === true) {
            logger.info(format('Connected to {} on {}', datastore.container, datastore.hosts));
        }
        bucket.on('error', function(error) {
            logger.error('Couchbase Error: ' + error);
        });
    });
    if (global.v8debug || datastore.hosts.length === 1) {
        bucket.operationTimeout = 120 * 1000;
        bucket.connectionTimeout = 120 * 1000;
    }
    return bucket;
};
