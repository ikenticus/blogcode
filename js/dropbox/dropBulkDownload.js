'use strict';

var async = require('async');
var fs = require('fs');
var request = require('request');
var path = require('path');

var cacheFile = path.basename(process.argv[1]) + 'on';
var album;

var downloadFile = function (info, callback){
    request.head(info.uri, function(err, res, body){
        if (err) {
            console.log(err);
        } else {
            console.log('Downloading', info.uri, '=>', info.filename);
            request(info.uri)
                .pipe(fs.createWriteStream(info.filename))
                .on('close', callback);            
        }
    });
};

var downloadImages = function (album) {
    var queue = async.queue(downloadFile, 15);
    queue.drain = function() {
        console.log('Queue finished');
    };

    album.forEach((a) => {
        var info = {
            filename: a.filename,
            uri: a.href.replace('dl=0', 'dl=1')
        }
        queue.push(info, function(err) {
            if (err) throw err;
        });
    });

    console.log('Queue Size:', queue.length());
    if (queue.length() === 0) console.log('Queue empty');
};

if (fs.existsSync(cacheFile)) {
    console.log('Reading album from cache file:', cacheFile);
    fs.access(cacheFile, fs.F_OK, function(err) {
        if (!err) {
            album = JSON.parse(fs.readFileSync(cacheFile).toString());
            downloadImages(album);
        }
    });
} else {
    var dropboxUrl = process.argv[2].split('?')[0];
    console.log('Downloading album from url:', dropboxUrl);
    request.get({
        url: dropboxUrl,
        qs: { dl: 0 }
    }, (err, res, body) => {
        if (!err) {
            var clean = body.replace(/^[.\s\S]*MODULE_CONFIG = /m, '').replace(/;<\/script>[.\s\S]*$/, '');
            album = JSON.parse(clean).modules.clean.init_react.components[0].props.contents.files;
            fs.writeFile(cacheFile, JSON.stringify(album, null, 4), (err) => {
                if (!err) downloadImages(album);
            });
        }
    });
}
