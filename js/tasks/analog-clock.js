/*
    Task: Analog Clock
*/
let format = require('string-format'),
    path = require('path');

function usage() {
    console.log(format('Calculate the angle betwwen hour and minute hands\nUsage: {} <HH:MM>', path.basename(process.argv[1])));
}

function degree (clock) {
    let hands = clock.split(':');
    let min = 6 * parseInt(hands[1]);
    let hour = parseInt(hands[0]);
        hour = (hour%12) * 30 + (min/12);
    return (hour < min) ? hour + 360 - min : hour - min;
}

// main
if (process.argv.length < 2) {
    usage();
    process.exit(1);
}
console.log(format('{} degrees', degree(process.argv[2])));
