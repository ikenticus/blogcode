/*
    Generate Windows CMD Script to Rename Episodes

    Usage: node moveEpisode.js dirlist.txt

        dirlist.txt is a cleaned list generated by: dir /b /s
        dirlist.json will be an episode list with kv: { ####: name }
*/

'use strict';

let _ = require('lodash'),
    format = require('string-format'),
    fs = require('fs'),
    path = require('path');

if (process.argv.length < 3) {
    console.log(format('Usage: {} dirlist.txt', path.basename(process.argv[1])));
    process.exit(0);
};


class Episodes {
    static processBase (data) {
        let max = data[0].split('\\');
        return max.slice(0, max.length - 1).join('\\') + '\\';
    }

    static removeBase (data, base) {
        let clean = [];
        data.forEach((d) => {
            if (d.split('\\').length > base.split('\\').length)
                clean.push(d.replace(base, ''));
        });
        return clean;
    }

    static removeSuffix (name, ext) {    
        return name.replace(new RegExp('.' + ext + '$', 'g'), '')
                   .replace(/\.AC3.*$/i, '')
                   .replace(/\.WS.*$/i, '')
                   .replace(/\.iNT.*$/i, '')
                   .replace(/\.DixX.*$/i, '')
                   .replace(/\.XviD.*$/i, '')
                   .replace(/\.DVDrip.*$/i, '')
                   .replace(/\.PROPER.*$/i, '');
    }

    static globalClean (name) {
        // replace all dots and underscores with spaces
        name = name.replace(/[\._]/g, ' ');
        let parts = name.split(' - '); // startcase if first character is lowercase
        if (parts.length > 1 && parts[1].charCodeAt(0) > 64)
            name = _.map(parts, (p) => { return _.startCase(p); }).join(' - ');
        return name;
    }

    static checkMapping (name, json) {
        if (_.endsWith(name, ' - ')) {
            let key = _.last(name.replace(/ - $/, '').split('\\'));
            //console.log('need to fix', name, 'with', json[key]);
            if (json[key]) name += json[key];
        }
        return name;
    }

    static buildClean (data, json) {
        let clean = {};
        data.forEach((d) => {
            let parts = d.split('\\');
            let dirname = parts.slice(0, parts.length - 1).join('\\') + '\\';
            let filename = _.last(parts);
            let ext = _.last(filename.split('.'));
            let name = this.removeSuffix(filename, ext);
            if (name.search(/[Ss]\d+[Ee]\d+-*[Ee]\d+/) > -1) {
                name = name.replace(/^.*[Ss]0*(\d+)[Ee](\d+)-*[Ee](\d+)\.*/, '$1$2-$3 - ');
            } else if (name.search(/[Ss]\d+[Ee]\d+/) > -1) {
                name = name.replace(/^.*[Ss]0*(\d+)[Ee](\d+)\.*/, '$1$2 - ');
            } else if (name.search(/\d+x\d+/) > -1) {
                name = name.replace(/^.*[^\d](\d+)x(\d+)\.*/, '$1$2 - ');
            }
            name = this.globalClean(name);
            if (json) name = this.checkMapping(name, json);
            clean[d] = dirname + name + '.' + ext.toLowerCase();
        });
        return clean;
    }
}

// MAIN
let filename = process.argv[2];
fs.readFile(filename, 'utf8', (err, raw) => {
    if (err) throw err;
    let data = raw.split(/[\r\n]/);
    let base = Episodes.processBase(data);
        data = Episodes.removeBase(data, base);

    let output = {};
    fs.readFile(filename.replace(/\.txt$/, '.json'), (err, raw) => {
        if (err) {
            output = Episodes.buildClean(data);
        } else {
            output = Episodes.buildClean(data, JSON.parse(raw));
        }
        _.forEach(output, (o, k) => {
            console.log(format('move "{}" "{}"', k, o));
        });
    });
});
