/*
    Task: Chatroom
*/
let _ = require('lodash'),
    format = require('string-format'),
    fs = require('fs'),
    numeral = require('numeral'),
    path = require('path');

function usage() {
    console.log(format('Display chatroom statistics\nUsage: %s <chatfile> <n>\n', path.basename(process.argv[1])));
}

function parse (data) {
    let stat = {};
	let lines = data.split('\n');
    _.forEach(lines, (c) => {
        if (c.length > 0) {
            let s = c.split(':', 2);
            let user = _.trim(s[0]),
                chat = _.trim(s[1]);

            if (!stat[user])
                stat[user] =  {
                    Count: 0,
                    Words: []
                };
            stat[user].Words = _.concat(stat[user].Words, chat.split(' '));
            stat[user].Count = stat[user].Words.length;
            stat[user].Name = user
        }
    });
	return stat;
}

function output (order, stat) {
    let most = !_.startsWith(order, '-');
    let mostWord = most ? 'most' : 'least';
    let rank = Math.abs(order);

    order = most ? 'desc' : 'asc';
    let user = _.orderBy(stat, 'Count', order);
    if (rank === 0) {
        console.log('List of %s wordy users:', mostWord);
        _.forEach(user, (u) => {
            console.log('%s %s', _.padStart(u.Count, 5, ' '), u.Name);
        });
    } else {
        console.log('The %s %s wordy user is (%s) with %d words',
            numeral(rank).format('0o'), mostWord,
            user[rank-1].Name, user[rank-1].Count);
    }
}

// MAIN
if (process.argv.length < 4) {
    usage();
    process.exit(1);
}

let chatfile = process.argv[2];
fs.readFile(chatfile, (err, data) => {
    if (err) {
        throw err;
        process.exit(1);
    }
    stat = parse(data.toString());
    output(process.argv[3], stat);
});
