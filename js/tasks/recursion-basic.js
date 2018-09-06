'use strict';

const fs = require('fs');

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', inputStdin => {
    inputString += inputStdin;
});

process.stdin.on('end', _ => {
    inputString = inputString.replace(/\s*$/, '')
        .split('\n')
        .map(str => str.replace(/\s*$/, ''));

    main();
});

function readLine() {
    return inputString[currentLine++];
}

// Multiply 'n' by 'k' using addition:
function nTimesK(n, k) {
    console.log('n:', n);
    if (n > 1) { // Recursive Case
        return k + nTimesK(n - 1, k);
    } else {    // Base Case n = 1
        return k;
    }
}

function main() {
    // export OUTPUT_PATH=/dev/stdout
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const nk = readLine().split(' ');

    const n = parseInt(nk[0], 10);

    const k = parseInt(nk[1], 10);

    let result = nTimesK(n, k);

    ws.write("Result: " + result + "\n");

    ws.end();
}

