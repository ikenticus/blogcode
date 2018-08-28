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

// Complete the minimumBribes function below.
function minimumBribes(q) {
    let bribes = 0;
    let moved = false;

    // more than 2 moves: Too chaotic
    for (let idx=0; idx< q.length; idx++) {
        let pos = q[idx];
        if ((pos - 1) - idx > 2)
            return 'Too chaotic';
    }

    // otherwise, execute bubble sort to count
    for (let i=0; i< q.length; i++) {
        for (let j=0; j< q.length; j++) {
            if (q[j] > q[j+1]) {
                let tmp = q[j]
                q[j] = q[j+1];
                q[j+1] = tmp;
                bribes++;
                moved = true;
            }
        }
        if (!moved) break;
        moved = false;
    }

    return bribes;
}

function main() {
    const t = parseInt(readLine(), 10);

    for (let tItr = 0; tItr < t; tItr++) {
        const n = parseInt(readLine(), 10);

        const q = readLine().split(' ').map(qTemp => parseInt(qTemp, 10));

        console.log(minimumBribes(q));
    }
}

