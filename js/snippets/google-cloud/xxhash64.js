// http://cyan4973.github.io/xxHash/

let _ = require('lodash'),
    converter = require('hex2dec');
    xxhash = require('xxhash');

const word = "teamstats_mlb_2017_2973";
const seed = 0;

/*
_.range(9).forEach(r => {
    console.log(converter.hexToDec(xxhash.hash64(new Buffer(word), 2**r, 'hex')));
});
*/

console.log(xxhash.hash64(Buffer(word), seed, 'hex'));
console.log(xxhash.hash64(Buffer(word, 'hex'), seed, 'hex'));
console.log(xxhash.hash64(Buffer(word, 'base64'), seed, 'hex'));

// cannot seem to get node.js xxhash to match Go/python result

