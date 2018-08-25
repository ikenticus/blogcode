'use strict';

const fs = require('fs');

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', inputStdin => {
    //inputString += inputStdin;
    // original code needed modification to fix excess spaces
    inputString += inputStdin.replace(/ +/g, ' ')
        .replace(/^\s+/, '');
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

// Complete the hourglassSum function below.
function hourglassSum(arr) {
    //console.log(arr);

    let hours = [];
    for (let r = 0; r < arr.length - 2; r++) {
        for (let c = 0; c < arr[r].length - 2; c++) {
            hours.push([
                arr[r][c], arr[r][c+1], arr[r][c+2],
                            arr[r+1][c+1],
                arr[r+2][c], arr[r+2][c+1], arr[r+2][c+2]
                ]);
        }
    }
    //console.log(hours);
    
    let max = -100; // do not initialize to zero for negative cases
    let sums = [];
    for (let r = 0; r < hours.length; r++) {
        sums[r] = 0;
        for (let c = 0; c < hours[r].length; c++) {
            sums[r] += hours[r][c];
        }
        if (sums[r] > max) max = sums[r];
    }
    //console.log(sums);
    
    return max;
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    let arr = Array(6);

    for (let i = 0; i < 6; i++) {
        arr[i] = readLine().split(' ').map(arrTemp => parseInt(arrTemp, 10));
    }

    let result = hourglassSum(arr);

    ws.write(result + "\n");

    ws.end();
}
