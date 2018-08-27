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

// Complete the minimumSwaps function below.
function minimumSwaps(arr) {
    let ord = arr.slice();
    ord.sort((a, b) => {
        return a - b; // ensure numerical sort
    });
    let swaps = 0;
    while (JSON.stringify(arr) !== JSON.stringify(ord)) {
        // 3. reducing ordered array items first allows method below
        let mix = [];
        arr.forEach((a, i) => {
            if (a !== ord[i]) {
                mix.push(a);
            }
        });
        arr = mix.slice();
        ord = mix.slice();
        ord.sort((a, b) => {
            return a - b; // ensure numerical sort
        });

        // 1. this method times out with 100k array items
        arr.forEach((a, i) => {
            if (a !== ord[i]) {
                swaps++;
                let j = ord.indexOf(a);
                arr[i] = arr[j];
                arr[j] = a;
            }
        });

        /*
        // 2. forEach => for still times out on 100k array
        for (let i = 0; i < arr.length; i++) {
            let a = arr[i];
            if (a !== ord[i]) {
                swaps++;
                let j = ord.indexOf(a);
                arr[i] = arr[j];
                arr[j] = a;
            }
        }
        */
    }
    return swaps;
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const n = parseInt(readLine(), 10);

    const arr = readLine().split(' ').map(arrTemp => parseInt(arrTemp, 10));

    const res = minimumSwaps(arr);

    ws.write(res + '\n');

    ws.end();
}

