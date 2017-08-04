'use strict';

var _ = require('lodash');
var fs = require('fs');
var path = require('path');

var walkSync = function(dir, filelist) {
    var files = fs.readdirSync(path.join(__dirname, dir));
    filelist = filelist || [];
    files.forEach(function(file) {
        if (fs.statSync(path.join(__dirname, dir, file)).isDirectory()) {
            filelist.push(walkSync(path.join(dir, file), []));
        } else if (_.endsWith(file, '.js')) {
            filelist.push(path.join(dir, file));
        }
    });
    return _.flatten(filelist);
};

var loadModules = function () {
    var modules = {};
    var jsFiles = walkSync('lib');

    _.forEach(jsFiles, function(j) {
        var modPath = j.replace(/^lib\//g, '')
        console.log(modPath, modPath.replace(/\.js$/, '').replace(/\//g, '.'), './lib/' + modPath);
        _.set(modules, modPath.replace(/\.js$/, '').replace(/\//g, '.'), require('./lib/' + modPath));
    });
    return modules;
};

module.exports = loadModules();
