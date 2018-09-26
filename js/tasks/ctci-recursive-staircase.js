'use strict';

const fs = require('fs');

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', inputStdin => {
    inputString += inputStdin;
});

process.stdin.on('end', function() {
    inputString = inputString.replace(/\s*$/, '')
        .split('\n')
        .map(str => str.replace(/\s*$/, ''));

    main();
});

function readLine() {
    return inputString[currentLine++];
}

let ways = {0:0, 1:1, 2:2, 3:4};
function stepPerms(n) {
    if (ways[n]) return ways[n];
    ways[n] = stepPerms(n-3) + stepPerms(n-2) + stepPerms(n-1);
    return ways[n];
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const s = parseInt(readLine(), 10);

    for (let sItr = 0; sItr < s; sItr++) {
        const n = parseInt(readLine(), 10);

        const res = stepPerms(n);

        ws.write(res + '\n');
    }

    ws.end();
}

