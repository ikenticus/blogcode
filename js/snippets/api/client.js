'use strict';

var _ = require('lodash');
var format = require('string-format');
var nickel = require('couchbase').N1qlQuery;

var Bucket = require('./bucket.js');
var eventHub = require('../event-hub.js');
var EVENTS = require('../events/constants.js');

var client = {};

function CouchbaseClient(datastore) {
    if (_.isEmpty(client)) {
        var dataBucket = new Bucket(datastore);

        /**
         * Assumes you will ALWAYS have a docId property on docContext
         * @param {Object} docContext
         * @returns {String}
         */
        client.keyBuilder = function keyBuilder(docContext) {
            return docContext.docId.toString();
        };

        /**
         * Return an key (or array of keys) from a docContext (or array of docContexts)
         * @param {Object|Object[]} docContext: contains all properties needed for key transformation
         * @returns {String|String[]}
         */
        client.getKey = function getKey(docContext) {
            var self = this;
            if (docContext instanceof Array) {
                return docContext.map(function (element) {
                    return self.keyBuilder(element);
                });
            }
            return self.keyBuilder(docContext);
        };

        /**
         * Get a single document by doc context, using CAS (check and set)
         * @param {Object} docContext: context to retrieve
         */
        client.getAndLockDoc = function getAndLockDoc(docContext) {
            var self = this;
            return new Promise(function (resolve) {
                dataBucket.getAndLock(self.getKey(docContext), docContext.options, function (error, result) {
                    if (error) resolve(error);
                    resolve(result);
                });
            });
        };

        /**
         * Get a single document by doc context
         * @param {Object} docContext: context to retrieve
         */
        client.getDoc = function getDoc(docContext) {
            return this.getMultiDoc([docContext]);
        };

        /**
         * MultiGet documents by doc context
         * @param {Object[]} docContexts: keys to retrieve
         */
        client.getMultiDoc = function getMultiDoc(docContexts) {
            var self = this;
            return new Promise(function (resolve) {
                var docKeys = self.getKey(docContexts);
                if (docKeys.length === 0) return resolve({});
                dataBucket.getMulti(docKeys, function (error, result) {
                    if (error > 0) {
                        var errorKeys = self._getErrorResultKeys(result);
                        self._getMultiReplica(errorKeys, function (replicaErr, replicaRes) {
                            var mergedResults = self._dictUpdate(result, replicaRes);
                            var orderedResult = self._orderResults(docKeys, mergedResults);
                            var preparedResult = self._prepareResults(orderedResult);
                            return resolve(preparedResult);
                        });
                    } else {
                        var orderedResult = self._orderResults(docKeys, result);
                        var preparedResult = self._prepareResults(orderedResult);
                        resolve(preparedResult);
                    }
                });
            });
        };

        /**
         * Upsert a document
         * @param {Object} docContext
         * @param {Object} docData
         */
        client.setDoc = function setDoc(docContext, docData) {
            var self = this;
            return new Promise(function (resolve, reject) {
                process.nextTick(dataBucket.upsert.bind(dataBucket, self.getKey(docContext),
                                 docData, docContext.options || {}, function (error, result) {
                    if (error) return reject([error, result]);
                    resolve(result);
                }));
            });
        };

        /**
         * MultiGet verison of bucket.getReplica - modeled after couchnode's multiget implementation
         * @param  {String[]}   keys     keys to attempt Replica read for
         * @param  {Function}   callback
         */
        client._getMultiReplica = function _getMultiReplica(keys, callback) {
            var replicaResults = {};
            var resCount = 0;
            var errCount = 0;
            keys.forEach(function (key) {
                dataBucket.getReplica(key, function (error, result) {
                    resCount++;
                    if (error) {
                        errCount++;
                        replicaResults[key] = {error: error};
                    } else {
                        replicaResults[key] = result;
                    }
                    if (resCount === keys.length) {
                        return callback(errCount, replicaResults);
                    }
                });
            });
        };

        /**
         * Sort a couchbase MuliResult based on the order of docKeys
         * @param  {Array} docKeys the document keys in the order you want the results
         * @param  {Object} results the couchbase MultiResult
         * @return {Object}         an ordered results object
         */
        client._orderResults = function _orderResults(docKeys, results) {
            var orderedResult = {};
            docKeys.forEach(function (docKey) {
                orderedResult[docKey] = results[docKey];
            });
            return orderedResult;
        };

        /**
         * Format MultiResult into docKey: result.value format
         * provides null for results with no value property
         * @param  {Object} results a CB MultiResult
         * @return {Object}         formatted results object
         */
        client._prepareResults = function _prepareResults(results) {
            var cleanResult = {};
            Object.keys(results).forEach(function (docKey) {
               cleanResult[docKey] = results[docKey].value || null;
            });
            return cleanResult;
        };

        /**
         * Return the keys for a couchbase MultiResult that have errors
         * @param  {Object} start   CB MultiResult
         * @return {String[]}       keys that had errors
         */
        client._getErrorResultKeys = function _getErrorResultKeys(start) {
            return Object.keys(start)
                .filter(function (key) {
                    return start[key].error;
                });
        };

        /**
         * Merge dictionaries akin to python's dict.update
         * Prioritize dict2 over dict1 (just like in python)
         * @param {Object} dict1
         * @param {Object} dict2
         */ // TODO: Replace this with Object.assign(dict1, dict2) when we switch to Node v4.2
        client._dictUpdate =  function dictUpdate(dict1, dict2) {
            var newDict = {};
            Object.keys(dict1 || {}).forEach(function (d1key) {
                newDict[d1key] = dict1[d1key];
            });
            Object.keys(dict2 || {}).forEach(function (d2key) {
                newDict[d2key] = dict2[d2key];
            });
            return newDict;
        };

        /**
         * Return the results from a couchbase N1QL query where:
         *  docContext { key1: value1 ... keyN: valueN }
         *  docOptions { view: name, limit: #, node: "page|feed|data" }
         */
        client.queryDoc = function queryDoc(docContext, docOptions) {
            var self = this;
            var queryString = format('SELECT meta().id, * FROM {}', docOptions.view);

            if (Object.keys(docContext).indexOf(docOptions.node) < 0) {
                queryString += self._queryFormat('WHERE', docOptions.node, 'NOT MISSING');
            } else {
                queryString += self._queryFormat('WHERE', docOptions.node, docContext[docOptions.node]);
                delete docContext[docOptions.node];
            }

            Object.keys(docContext).forEach(function (key) {
                queryString += self._queryFormat('AND', key, docContext[key]);
            });

            if (docOptions.sort) {
                if (docOptions.order) {
                    queryString += format(' ORDER BY {} {}', docOptions.sort, docOptions.order);
                } else {
                    queryString += format(' ORDER BY {}', docOptions.sort);
                }
            }
            if (docOptions.limit) {
                queryString += format(' LIMIT {}', docOptions.limit);
            }
            if (docOptions.offset) {
                queryString += format(' OFFSET {}', docOptions.offset);
            }

            //console.log(queryString);
            var query = nickel.fromString(queryString);
            return new Promise(function (resolve, reject) {
                dataBucket.query(query, function (error, result) {
                    if (error) {
                        return reject([error, result]);
                    }
                    var results = [];
                    result.forEach(function (item) {
                        results.push(item);
                    });
                    resolve(results);
                });
            });
        };

        client._queryFormat = function _queryFormat(word, key, value) {
            if (_.isInteger(value)) {
                return format(' {} {} = {}', word, key, value);
            } else if (value.toUpperCase().indexOf('MISSING') >= 0) {
                return format(' {} {} IS {}', word, key, value.toUpperCase());
            } else if (value.indexOf('!') === 0) {
                return format(' {} {} != "{}"', word, key, value.substring(1));
            } else if (value.indexOf('~') === 0) {
                return format(' {} {} LIKE "{}"', word, key, value.substring(1));
            } else if (value.indexOf('^') === 0) {
                return format(' {} {} NOT LIKE "{}"', word, key, value.substring(1));
            } else if (value.indexOf('>') === 0) {
                return format(' {} ("{}" IN {} OR {} = "{}")', word,
                        value.substring(1), key, key, value.substring(1));
            } else if (['true', 'false'].indexOf(value.toLowerCase()) >= 0) {
                return format(' {} {} = {}', word, key, JSON.parse(value));
            } else {
                return format(' {} {} = "{}"', word, key, value);
            }
        };

        /**
         * Return the results from a couchbase N1QL querystring
         */
        client.queryString = function queryString(queryString) {
            //console.log(queryString);
            var query = nickel.fromString(queryString);
            return new Promise(function (resolve, reject) {
                dataBucket.query(query, function (error, result) {
                    if (error) {
                        return reject([error, result]);
                    }
                    var results = [];
                    result.forEach(function (item) {
                        results.push(item);
                    });
                    resolve(results);
                });
            });
        };

        dataBucket.on('connect', function cbClientReady() {
            eventHub.emit(EVENTS.CB_CLIENT_READY, {name: dataBucket._name, hosts: datastore.hosts});
        });

        dataBucket.on('error', function cbErrorEvent(err) {
            eventHub.emit(EVENTS.CB_CLIENT_ERROR, {name: dataBucket._name, error: err});
        });
    }
    return client;
}

module.exports = CouchbaseClient;
