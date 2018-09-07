'use strict';

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



function main() {
    let arr = Array(6);

    for (let i = 0; i < 6; i++) {
        arr[i] = readLine().split(' ').map(arrTemp => parseInt(arrTemp, 10));
    }

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
    
    let max = -100; // do not initialize to zero for negative cases
    let sums = [];
    for (let r = 0; r < hours.length; r++) {
        sums[r] = 0;
        for (let c = 0; c < hours[r].length; c++) {
            sums[r] += hours[r][c];
        }
        if (sums[r] > max) max = sums[r];
    }
    
    console.log(max);
}

