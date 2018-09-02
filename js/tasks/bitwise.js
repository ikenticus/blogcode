'use strict';

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', inputStdin => {
    inputString += inputStdin;
});

process.stdin.on('end', _ => {
    inputString = inputString.trim().split('\n').map(string => {
        return string.trim();
    });
    
    main();    
});

function readLine() {
    return inputString[currentLine++];
}

function getMaxLessThanK(n, k) {
    // short method suggested in discussion
    return ((k | (k - 1)) > n) ? (k - 2) : (k - 1);

    // the long method seems to fail on testcase2+
    let mab = 0;
    for (let a = 0; a < n - 1; a++) {
       for (let b = 1; b < n; b++) {
           if ((a & b) < k && mab < (a & b))
               mab = a & b;
       } 
    }
    return mab;
}

function main() {
    const q = +(readLine());
    
    for (let i = 0; i < q; i++) {
        const [n, k] = readLine().split(' ').map(Number);
        
        console.log(getMaxLessThanK(n, k));
    }
}
