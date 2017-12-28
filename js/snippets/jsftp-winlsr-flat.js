var _ = require('lodash');
var async = require('async');
var format = require('string-format');
var JSFtp = require('jsftp');
var moment = require('moment');
var path = require('path');
var site = {
    host: 'mft.gannett.com',
    user: 'sportsrelaunch',
    pass: 'sptrlch13'
};

var DIR_NAME = '<DIR>';
var ftp = new JSFtp(site);

function _lsrFindPath(data, obj, _prefix) {
    var prefix = _prefix ? path.join(_prefix, data.name) : data.name;
    if (data == obj) {
        return prefix;
    }
    for(var i = 0; i < data.children.length; ++i) {
        if (data.children[i] === obj) {
            return path.join(prefix, data.children[i].name);
        }

        if (data.children[i].children) {
            var result = _lsrFindPath(data.children[i], obj, prefix);
            if (result) return result;
        }
    }

    return null;
}

function winlsr(ftp, root, callback, isFlat) {

    var result = [{
        name: '.',
        size: DIR_NAME
    }];
    var curDir = result[0];
    var flat = [];

    async.doWhilst(
        function iter (icallback) {
            var _path = _lsrFindPath(result[0], curDir, root);

            ftp.list(_path, (err, data) => {
                if (err) return icallback(err);
                curDir.children = _.chain(data.split('\r\n'))
                                   .map((r) => {
                                        let stats = _.compact(r.split(' '));
                                        if (!_.isEmpty(stats))
                                            return {
                                                name: _.last(stats),
                                                size: _.nth(stats, -2),
                                                time: moment(new Date(format('{} {}', stats[0], stats[1].replace(/[AP]M/, ' $&'))))
                                            };
                                        })
                                   .compact()
                                   .value();
                flat = _.concat(flat,
                            _.chain(curDir.children)
                             .map((c) => {
                                    c.rdir = _path;
                                    if (c.size !== DIR_NAME)
                                        return _.omit(c, 'children'); 
                                })
                             .compact()
                             .value()
                        );
                icallback();
            });

        }, function test (arg) {
            var _result = arg || result;

            return _result.some (function(item) {
                if (item.size === DIR_NAME && !item.children) {
                    curDir = item;
                    return true;
                }
                if (item.size === DIR_NAME) {
                    return test(item.children); // If directory has children.
                }

                return false; // If item is not directory.
            })
        }, function done (err) {
            if (err) return callback(err);
            if (isFlat) {
                callback(null, flat || []);
            } else {
                callback(null, result || []);
            }
        })
}

var root = 'XML';
winlsr(ftp, root, (err, data) => {
    console.log(JSON.stringify(data, null, 4));
}, true);
