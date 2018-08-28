'use strict';

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

// Complete the checkMagazine function below.
function checkMagazine(magazine, note) {
    let scraps = {};
    magazine.forEach((m) => {
        scraps[m] = scraps[m] ? scraps[m] + 1 : 1;
    });

    # avoid forEach to avoid async closure
    for (let n = 0; n < note.length; n++) {
        let word = note[n];
        if (scraps[word] && scraps[word] > 0) {
            scraps[word] -= 1;
        } else {
            console.log('No');
            return
        }
    };
    console.log('Yes');
}

function main() {
    const mn = readLine().split(' ');

    const m = parseInt(mn[0], 10);

    const n = parseInt(mn[1], 10);

    const magazine = readLine().split(' ');

    const note = readLine().split(' ');

    checkMagazine(magazine, note);
}

