// Hard
// https://www.hackerrank.com/challenges/game-of-throne-ii/problem

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

function factorial(N) {
    return (N === 0) ? 1 : N * factorial(N-1);
}    

// Complete the solve function below.
function solve(s) {
    // fails for large words: N! / (a! * b! * c!)
    let cnt = {};
    s.split('').forEach((c) => {
        cnt[c] = (cnt[c] || 0) + 1;
    });
    //console.log(cnt);

    let k = Object.keys(cnt);
    let n = 0;
    let d = [];
    k.forEach((c) => {
        let half = parseInt(cnt[c] / 2);
        n += half;
        d.push(factorial(half));
    });
    //console.log(n, d);
    return factorial(n) / d.reduce((a, b) => a * b, 1);
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const s = readLine();

    let result = solve(s);

    ws.write(result + "\n");

    ws.end();
}

