// Medium
// https://www.hackerrank.com/challenges/sherlock-and-anagrams/problem

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

function compare(w1, w2) {
    let h1 = {};
    let h2 = {};

    /*
    // comparing hash does not compare properly
    // time 11s locally
    for (let c = 0; c < w1.length; c++) {
        h1[w1[c]] = (h1[w1[c]] || 0) + 1;
        h2[w2[c]] = (h2[w2[c]] || 0) + 1;
    }
    */

    /*
    // comparing alphabetically ordered hash times out for Testcase(s) 2-5
    // time 21s locally
    for (let c = 97; c < 124; c++) {
        h1[String.fromCharCode(c)] = 0;
        h2[String.fromCharCode(c)] = 0;
    }
    for (let c = 0; c < w1.length; c++) {
        h1[w1[c]]++;
        h2[w2[c]]++;
    }
    */

    return JSON.stringify(h1) === JSON.stringify(h2);
}

// Complete the sherlockAndAnagrams function below.
function sherlockAndAnagrams(s) {
    let words = 0;

    for (let c = 1; c < s.length; c++) { // character length loop
        for (let i1 = 0; i1 < s.length - c; i1++) { // word1 loop
            for (let i2 = i1 + 1; i2 < s.length - c + 1; i2++) { // word2 loop
                let w1 = s.slice(i1, i1 + c);
                let w2 = s.slice(i2, i2 + c);

                // iteration count times out for Testcase(s) 4-5
                // time 12s locally
                if (w1.split('').sort().join('') === w2.split('').sort().join('')) words++;
                
                // attempts at JSON/hash comparisons not better
                //if (compare(w1, w2)) words++;
            }    
        }
    }

    return words;
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const q = parseInt(readLine(), 10);

    for (let qItr = 0; qItr < q; qItr++) {
        const s = readLine();

        let result = sherlockAndAnagrams(s);

        ws.write(result + "\n");
    }

    ws.end();
}

