// Easy
// https://www.hackerrank.com/challenges/caesar-cipher-1/problem

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

// Complete the caesarCipher function below.
function caesarCipher(s, k) {
    let a = 'abcdefghijklmnopqrstuvwxyz';
    let m = k % a.length;
    let c = a.slice(m).concat(a.slice(0, m));
    let x = [];
    for (let i = 0; i < s.length; i++) {
        let n = a.indexOf(s[i]);
        if (n > -1) {
            x.push(c[n]);            
        } else {
            n = a.indexOf(s[i].toLowerCase());
            if (n > -1) {
                x.push(c[n].toUpperCase());               
            } else {
                x.push(s[i]);                
            }
        }
    }
    return x.join('');
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    const n = parseInt(readLine(), 10);

    const s = readLine();

    const k = parseInt(readLine(), 10);

    let result = caesarCipher(s, k);

    ws.write(result + "\n");

    ws.end();
}

