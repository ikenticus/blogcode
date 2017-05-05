/*
    Clean up pasted wikipedia episodes

    Usage: node wikiEpisodes.js eplist.txt

        deplist.txt is a copy-and-pasted wikipedia episode list (including Season # headers)
*/

'use strict';

let _ = require('lodash'),
    format = require('string-format'),
    fs = require('fs'),
    path = require('path');

if (process.argv.length < 3) {
    console.log(format('Usage: {} eplist.txt', path.basename(process.argv[1])));
    process.exit(0);
};

// MAIN
let filename = process.argv[2];
fs.readFile(filename, 'utf8', (err, raw) => {
    if (err) throw err;
    let data = raw.split(/[\r\n]/);

    let output = {};
    let season = 0;
    data.forEach((d) => {
        if (_.startsWith(d, 'Season')) season = parseInt(d.replace(/^Season (\d+).*$/, '$1'));
        let clean = d.replace(/\[\w\]/, '')
        if (clean.search(/^\d+\s+(\d+)\s+"([^"]+)".*$/) > -1) {
            if (season > 0) {
                let ep = clean.replace(/^\d+\s+(\d+)\s+"([^"]+)".*$/, '$1|$2').split('|');
                let key = format('{}{}', season, _.padStart(ep[0], 2, '0'));
                output[key] = ep[1];
            }            
        } else if (clean.search(/^(\d+)\s+"([^"]+)".*$/) > -1) { // multipart
            if (season > 0) {
                let ep = clean.replace(/^(\d+)\s+"([^"]+)".*$/, '$1|$2').split('|');
                let key = format('{}{}-{}', season, _.padStart(parseInt(ep[0]) - 1, 2, '0'), _.padStart(ep[0], 2, '0'));
                output[key] = ep[1];

                let key1 = format('{}{}', season, _.padStart(parseInt(ep[0]) - 1, 2, '0'));
                let key2 = format('{}{}', season, _.padStart(ep[0], 2, '0'));
                output[key1] = ep[1] + ', Part 1';
                output[key2] = ep[1] + ', Part 2';
            }
        }
    });
    console.log(output);
    if (process.argv[3]) {
        fs.writeFile(filename.replace(/\.txt$/, '_list.txt'),
            _.map(output, (o, k) => { return format('{} - {}', k, o); }).join('\n'));
    } else {
        fs.writeFile(filename.replace(/\.txt$/, '.json'),
            JSON.stringify(output, null, 4));
    }
});
