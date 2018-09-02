// Easy
// https://www.hackerrank.com/challenges/weighted-uniform-string/problem

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

// Complete the weightedUniformStrings function below.
function weightedUniformStrings(s, queries) {
    let u;
    let w = [];
    for (let c = 0; c < s.length; c++) {
        if (c == 0 || s[c] != s[c-1]) u = 0;
        u += s[c].charCodeAt(0) - 96;
        w.push(u);
    }
    
    let r = [];
    for (let q = 0; q < queries.length; q++) {
        r.push(w.includes(queries[q]) ? 'Yes' : 'No');    
    }
    return r;
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const s = readLine();

    const queriesCount = parseInt(readLine(), 10);

    let queries = [];

    for (let i = 0; i < queriesCount; i++) {
        const queriesItem = parseInt(readLine(), 10);
        queries.push(queriesItem);
    }

    let result = weightedUniformStrings(s, queries);

    ws.write(result.join("\n") + "\n");

    ws.end();
}

