const N = 15;

let _ = require('lodash');
let request = require('request');

const url = 'https://gist.githubusercontent.com/zach-karat/dd26fe2387c1f687f655abcca1d688d7/raw/b38f34e31ecd9fd4c3a870722ef321d7d16ef54e/gistfile1.txt'

let dict = {};
request.get(url, (err, res, body) => {
  _.forEach(body.split('\n'), (b) => {
    if (!dict[b]) {
      dict[b] = 1;
    } else {
      dict[b] += 1;
    }
  });

  let sorted = _.values(dict);
  sorted.sort((a, b) => {return a-b;});
  let top = _.takeRight(sorted, N);

  let newlist = [];
  _.forEach(dict, (v, k) => {
    if (top.indexOf(v) > -1) newlist.push({count: v, url: k});
  });
  
  _.forEach(_.orderBy(newlist, 'count', 'desc'), (n) => {
    console.log(n.count, n.url);
  });

});

/*
// JKL alternative
var request = require('request');
var log_url = 'https://gist.githubusercontent.com/zach-karat/dd26fe2387c1f687f655abcca1d688d7/raw/b38f34e31ecd9fd4c3a870722ef321d7d16ef54e/gistfile1.txt';

var top_n = 5;

request(log_url, { json: false }, (err, res, body) => {
    if (err) { return console.log(err); }

    let urls = {};

    body.split('\n').forEach((url) => {
        if (urls[url]) { urls[url].count++; }
        else { urls[url] = { count: 1 }; }
    });
    let top_urls = [];
    let keys = Object.keys(urls);
    let url, count;

    for(let n = 0; n < top_n; n++) {
        count = 0;
        keys.forEach((k) => {
            if (urls[k].selected) { return; }

            if (urls[k].count > count) {
                url = k;
                count = urls[k].count;
            }
        });
        urls[url].selected = true;
        top_urls.push({ url: url, count: count });
    }
    console.log(JSON.stringify(top_urls, null, 4));
});
*/
