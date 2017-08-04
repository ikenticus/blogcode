'use strict';
// tools.js is used for unit testing and TeamCity mocha fails on ES6 (s) => notation
// make sure all functions are explicitly written as function (s) in this library

var _ = require('underscore');
    _.str = require('underscore.string');
var csv = require('csv');
var config = require('config');
var format = require('string-format');
var JSFtp = require('jsftp');
var request = require('request');

var ingress = require('./ingress.js')();
var logger = require('./logger.js')();

var paramList = {
    'feed': [ 'subcategory', 'sport', 'subsport', 'type', 'typeId' ],
    'legacy': [ 'consumer', 'service', 'legacy' ],
    'metadata': [ 'sport', 'season', 'type' ],
    'universal': [ 'sport', 'subsport', 'season', 'type', 'typeId', 'subtype', 'subtypeId' ]
};

var csv2json = function (data, sep, callback) {
    csv.parse(data, {columns: true, delimiter: sep}, function (err, json) {
        if (!err && callback) callback(json);
        return data;
    });
};

var json2csv = function (json, sep, callback) {
    csv.stringify(json, {header: true, delimiter: sep}, function (err, data) {
        if (!err && callback) callback(data);
        return json;
    });
};

var sportName = function (subsport) {
    switch (subsport[4]) {
        case 'B':
        case 'W': return 'basketball';
        case 'F': return 'football';
        default: return 'baseball';
    }
};

var slugify = function (value) {
    return _.str.slugify(value);
};

var buildDocId = function (feed) {
    // iterate thru the {} params and write the page_v1_* docs first
    var consumer = feed.consumer || 'universal';
    var docId = format('page_v1_{}', consumer);

    paramList[consumer].forEach(function (param) {
        if (feed[param]) docId += format('_{}', slugify(feed[param]));
    });
    return docId;
};

var parseDocId = function (docId, showConsumer) {
    var feed = {};
    if (docId.indexOf('/') === 0) docId = docId.slice(1);
    var keys = docId.split(/[_\/]/);

    var consumer = keys[0];
    var offset = 1;
    if (consumer === 'page') {
        consumer = keys[2];
        offset = 3;
    }

    paramList[consumer].forEach(function (pkey) {
        if (consumer === 'metadata' && (keys.length - paramList[consumer].length) === 2) {
            if (paramList[consumer].indexOf(pkey) === 2) {
                offset = 2;
                delete feed[paramList[consumer][1]];
            }
        }
        var value = keys[paramList[consumer].indexOf(pkey) + offset];
        if (showConsumer != null)
            feed.consumer = consumer;
        if (value) {
            feed[pkey] = value;
            if (pkey === 'subsport')
                feed[pkey] = feed[pkey].toUpperCase();
        }
    });
    return feed;
};

var getMultiDocs = function (docContexts, simplify, callback) {
    var logText = format('Getting {}: ', JSON.stringify(docContexts));
    //logger.info(logText + 'started');
    ingress.multiget(docContexts)
        .then(function (result) {
            //logger.info(logText + result);
            if (simplify) { // simplify the result keys
                _.forEach(result, function (data, key) {
                    var newKey = '';
                    simplify.forEach(function (s) { // if data is null, determine key from docId
                        //if (!data && key.indexOf('livescores') < 0) console.log('Empty', key);
                        var valid = data ? data[s] : parseDocId(key)[s];
                        if (valid) newKey += valid;
                    });
                    result[newKey] = data;
                    delete result[key];
                });
            }
            callback(result);
        })
        .catch(function (err) {
            logger.error(logText + ' ' + err);
        });
};

var publishPrintXML = function (urlPath) {
    logger.info('publishing', config.publish + config.legacy.print + urlPath);
    request({
        method: 'GET',
        url: config.publish + config.legacy.print + urlPath
    }, function (error, response) {
        if (error) {
            logger.error('Publishing', response.request.path, error);
        } else {
            logger.info('Publishing', response.request.path, 'SUCCESS');
        }
        return response;
    });
};

var queryDocs = function (docContext, docOptions, callback) {
    var logText = format('Querying {}: ', JSON.stringify(docContext));
    ingress.query(docContext, docOptions)
        .then(function (result) {
            logger.info(logText + result);
            callback(result);
        })
        .catch(function (err) {
            logger.error(logText + ' ' + err);
        });
};

var saveDoc = function (docId, feed, callback) {
    var logText = format('Setting {}: ', docId);
    ingress.set(docId, feed)
        .then(function (result) {
            logger.info(logText + result);
            if (callback) callback(result, null);
        })
        .catch(function (error) {
            logger.error(logText + error);
            if (callback) callback(null, error);
        });
};

var saveFTP = function (site, name, data) {
    var ftp = new JSFtp(config.ftp[site]);
    var buffer = new Buffer(data);
    var logText = format('FTPing {}: ', name);
    ftp.put(buffer, config.ftp[site].rdir + name, function(error) {
        if (error) {
            logger.error(logText, error);
        } else {
            logger.info(logText + 'success!');
        }
        ftp.raw.quit();
    });
};

var saveLatestSeason = function (docId, feed, callback) {
    var season = feed.season;
    var logText = format('Getting Latest {}: ', docId);
    ingress.get(docId)
        .then(function (result) {
            if (!result[docId] || season >= result[docId].season) {
                logText = format('Setting Latest {}: ', docId);
                ingress.set(docId, feed)
                    .then(function (result) {
                        logger.info(logText + result);
                        if (callback) callback(feed);
                    })
                    .catch(function (error) {
                        logger.error(logText + error);
                    });
            }
        })
        .catch(function (error) {
            logger.error(logText + error);
        });
};

var saveLatestTypeId = function (feed, callback) {
    var typeId = feed.typeId;
    feed.latest = typeId;
    if (feed.subtypeId) { // for type/yyyymmdd/subtype/#
        feed.typeId = feed.subtypeId;
        delete feed.subtypeId;
        delete feed.subtype;
    } else {
        delete feed.typeId;
    }
    var docId = buildDocId(feed);
    var logText = format('Getting Latest {}: ', docId);
    ingress.get(docId)
        .then(function (result) {
            if (!result[docId] || typeId >= result[docId].latest) {
                logText = format('Setting Latest {}: ', docId);
                ingress.set(docId, feed)
                    .then(function (result) {
                        logger.info(logText + result);
                        if (callback) callback(feed);
                    })
                    .catch(function (error) {
                        logger.error(logText + error);
                    });
            }
        })
        .catch(function (error) {
            logger.error(logText + error);
        });
};

var upsertDoc = function (docId, callback) {
    ingress.lockget(docId)
        .then(function (result) {
            if (result.code && result.code === 11) {
                upsertDoc(docId, callback);
            } else {
                callback(result);
                var logText = format('Setting {} ({}): ', docId, result.cas);
                ingress.set(docId, result.value, result.cas)
                    .then(function (answer) {
                        logger.info(logText + answer);
                    })
                    .catch(function (error) {
                        logger.error(logText + error);
                    });
            }
        })
        .catch(function (error) {
            logger.error(format('Getting {}: {}', docId, error));
        });
};

module.exports = {
    buildDocId: buildDocId,
    csv2json: csv2json,
    getMultiDocs: getMultiDocs,
    json2csv: json2csv,
    paramList: paramList,
    parseDocId: parseDocId,
    publishPrintXML: publishPrintXML,
    queryDocs: queryDocs,
    saveDoc: saveDoc,
    saveFTP: saveFTP,
    saveLatestSeason: saveLatestSeason,
    saveLatestTypeId: saveLatestTypeId,
    slugify: slugify,
    sportName: sportName,
    upsertDoc: upsertDoc
};
