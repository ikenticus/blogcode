// Medium
// https://www.hackerrank.com/challenges/the-power-sum/problem

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

// Complete the powerSum function below.
function powerSum(X, N) {
    //return recurseUp(X, N, 1);
    
    //let root = Math.sqrt(X);
    let root = Math.floor(Math.pow(Math.abs(X), 1/N));
    return recurseDn(X, N, root);
}

// recursion decrementing from SQRT(X) to 1
// Can we recurse downward? How to continue once criteria is met?
function recurseDn(X, N, i) {
//    console.log('  DN with', X, ':', i + '^' + N);
    let iN = i**N;
    if (i < 1) {
        return 0;
    } else if (iN == X) {
        return (i > 0) ? 1 + recurseDn(X, N, i-1) : 1;
/*
        console.log(i + '^' + N, '==', X, '\n=====\n');
        if (i > 0) {
            console.log('  ', i + '^' + N, '<', X, 'TEST with', i-1);
            return 1 + recurseDn(X, N, i-1);
        }
        return 1;
*/
    } else {
//        console.log('  ', i + '^' + N, '<', X, 'TEST with', i-1);
        return recurseDn(X, N, i-1) + recurseDn(X-iN, N, i-1);
    }
}

// recursion incrementing from 1 to ...
function recurseUp(X, N, i) {
//    console.log('  UP with', X, ':', i + '^' + N);
    let iN = i**N;
    if (iN > X) {
//        console.log('    OVER', i + '^' + N, '>', X);
        return 0;
    } else if (iN == X) {
//        console.log(i + '^' + N, '==', X, '\n=====\n');
        return 1;
    } else {
//        console.log('  ', i + '^' + N, '<', X, 'TEST with', i+1);
        return recurseUp(X, N, i+1) + recurseUp(X-iN, N, i+1);
    }
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const X = parseInt(readLine(), 10);

    const N = parseInt(readLine(), 10);

    let result = powerSum(X, N);

    ws.write(result + "\n");

    ws.end();
}

