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

// Complete the arrayManipulation function below.
function arrayManipulation(n, queries) {
    /*
    // this method times out with 10k queries
    let arr = Array(n);
    for (let i = 0; i < n; i++) {
        arr[i] = 0;
    }
    for (let q = 0; q < queries.length; q++) {
        let [a, b, k] = queries[q]
        for (let i = a; i <= b; i++) {
            arr[i-1] += k;
        }
        //console.log('ARR', arr);
    }
    return Math.max(...arr);
    */

    // https://codereview.stackexchange.com/questions/95755/algorithmic-crush-problem-hitting-timeout-errors
    const _ = require('lodash');
    let arr = _.fill(Array(n+1), 0);
    _.forEach(queries, (q) => {
        let [a, b, k] = q
        // calculate differance array
        arr[a-1] += k;
        arr[b] -= k;
    });
    let max = 0,
        sum =0;
    _.forEach(arr, (i) => {
        // determine max using prefix sum
        sum += i
        if (sum > max)
            max = sum;
    });
    return max;
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const nm = readLine().split(' ');

    const n = parseInt(nm[0], 10);

    const m = parseInt(nm[1], 10);

    let queries = Array(m);

    for (let i = 0; i < m; i++) {
        queries[i] = readLine().split(' ').map(queriesTemp => parseInt(queriesTemp, 10));
    }

    let result = arrayManipulation(n, queries);

    ws.write(result + "\n");

    ws.end();
}
