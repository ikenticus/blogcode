// Easy
// https://www.hackerrank.com/challenges/between-two-sets/problem

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
    inputString = inputString.trim().split('\n').map(str => str.trim());

    main();
});

function readLine() {
    return inputString[currentLine++];
}

/*
 * Complete the getTotalX function below.
 */
function getTotalX(a, b) {
    // sort from low to high
    a.sort();
    b.sort();

    function gcd (x, y) {
        return !y ? x : gcd(y, x % y);
    }

    let fA = [];
    let lcm = a[0];
    a.forEach((n) => {
       lcm = (lcm * n) / gcd(lcm, n);
    });
    for (let i = lcm; i <= b[0]; i += lcm) {
        fA.push(i); 
    }
    
    let fB = [];
    let inc = b[0] % 2 === 0 ? 1 : 2;
    for (let i = lcm; i <= b[0]; i += 1) {
        let fact = true;
        for (let j = 0; j < b.length; j++) {
            if (b[j] % i > 0) fact = false;
        }
        if (fact) fB.push(i);
    }

    let A = new Set(fA);
    let B = new Set(fB);
    let between = new Set([...A].filter(x => B.has(x)));
    console.log(a, b, lcm, A, B, between);
    return between.size;
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const nm = readLine().split(' ');

    const n = parseInt(nm[0], 10);

    const m = parseInt(nm[1], 10);

    const a = readLine().split(' ').map(aTemp => parseInt(aTemp, 10));

    const b = readLine().split(' ').map(bTemp => parseInt(bTemp, 10));

    let total = getTotalX(a, b);

    ws.write(total + "\n");

    ws.end();
}

