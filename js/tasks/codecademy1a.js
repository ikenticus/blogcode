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
  
  let max = _.max(_.values(dict));
  _.forEach(dict, (v, k) => {
    if (v === max) console.log(v, k);
  });
});
