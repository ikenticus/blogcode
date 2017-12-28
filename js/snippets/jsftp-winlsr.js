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

var FTP_DIR_TYPE = '<DIR>';
var ftp = new JSFtp(site);

function _lsrFindPath(data, obj, _prefix) {
    var prefix = _prefix ? path.join(_prefix, data.name) : data.name;
    if(data == obj) {
        return prefix;
    }
    for(var i = 0; i < data.children.length; ++i) {
        if(data.children[i] === obj) {
            return path.join(prefix, data.children[i].name);
        }

        if(data.children[i].children) {
            var result = _lsrFindPath(data.children[i], obj, prefix);
            if (result) return result;
        }
    }

    return null;
}

function winlsr(ftp, root, callback) {

    var result = [{
        size: FTP_DIR_TYPE,
        name: "."
    }];
    var currentDirectory = result[0];

    async.doWhilst(
        function iter(clb) {
            var _path = _lsrFindPath(result[0], currentDirectory, root);

            ftp.list(_path, function(err, data) {
                if(err) return clb(err);
                currentDirectory.children = _.chain(data.split('\r\n'))
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
                clb();
            })

        }, function test(arg) {
            var _result = arg || result;

            return _result.some(function(item) {
                if(item.size === FTP_DIR_TYPE && !item.children) {
                    currentDirectory = item;
                    return true;
                }
                if(item.size === FTP_DIR_TYPE) {
                    return test(item.children); // If directory has children.
                }

                return false; // If item is not directory.
            })
        }, function done(err) {
            if (err) return callback(err);
            callback(null, result || []);
        })
}

winlsr(ftp, 'XML', (err, data) => {
    console.log(JSON.stringify(data, null, 4));
})
