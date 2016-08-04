var moment = require('moment-timezone');
var util = require('util');

var format = 'YYYY-MM-DD HH:mm:ss'
var now = new Date();
console.log('Current time is:', moment(now).format(format));
console.log('UTC/GMT becomes:', moment(now).tz('UTC').format(format));

if (process.argv.length > 2) {
    var ask = process.argv[2];
    if (ask == 'all') {
        console.log(moment.tz.names());
    } else {
        console.log(ask + ':', moment(now).tz(ask).format(format));
    }
}

