// Easy
// https://www.hackerrank.com/challenges/separate-the-numbers/problem

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

// Complete the separateNumbers function below.
function separateNumbers(s) {
    for (let c = 1; c <= s.length/2; c++) {
        let a = s.slice(0, c);
        //console.log('CHECK', a);

        let pre = '';
        /*
        // splitting on zeroes is randomly dangerous
        if (a.indexOf('0') > 10) {
            let parts = a.split('0');
            let last = (parts.slice(-1).length < 5) ? -2 : -1;
            pre = parts.slice(0, last).join('0') + '0';
            a = parts.slice(last).join('0');
        } 
        */
        if (a.length > 10) {
            pre += a.slice(0, -10);
            a = a.slice(-10);
            // shift the leading zeroes from a to trail pre
            while (a.length > 1 && a.indexOf('0') == 0) {
                pre += '0';
                a = a.slice(1);
            }
        }
        //console.log('CHECK', pre, a);

        let test = [];
        for (let x = 0; x <= s.length/a.length; x++) {
            // javascript integer limited to 2^52 = 4503599627370496
            // so the parseInt + x fails for 9007199254740992, etc...
            /*
            test.push(parseInt(a) + x);
            let word = '';
            test.forEach((t) => {
                word += t.toString();
            });
            */
            test.push(pre + (parseInt(a) + x).toString());
            let word = test.join('');

            /*
            // DEBUG
            if (pre.length > 0) {
                console.log('TEST0', test);
                console.log('TESTs', s, s == word);
                console.log('TESTw', word, s == word);
            }
            */

            if (s == word) {
                console.log('YES', pre + a);
                return;
            }
        }
    }
    console.log('NO');
}

function main() {
    const q = parseInt(readLine(), 10);

    for (let qItr = 0; qItr < q; qItr++) {
        const s = readLine();

        separateNumbers(s);
    }
}

