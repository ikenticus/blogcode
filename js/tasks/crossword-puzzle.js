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

function check(crossword, word) {
    let slots = [];
    for (let row = 0; row < 10; row++) {
        for (let col = 0; col < 10; col++) {
            let validH = true;
            let validV = true;
            for (let w = 0; w < word.length; w++) {
                if (col <= 10 - word.length)
                    if (['-', word[w]].indexOf(crossword[row][col + w]) < 0)
                        validH = false;
                if (row <= 10 - word.length)
                    if (['-', word[w]].indexOf(crossword[row + w][col]) < 0)
                        validV = false;
            }
            
            if (validH && col <= 10 - word.length)
                slots.push([row, col, 'H']);
            if (validV && row <= 10 - word.length)
                slots.push([row, col, 'V']);
        }
    }
    return slots;
}

function writePuzzle(crossword, word, slot, empty = false) {
    let [row, col, dir] = slot;
    for (let w = 0; w < word.length; w++) {
        let letter = empty ? empty : word[w];
        if (dir === 'H') {
            crossword[row][col + w] = letter;
        } else {
            crossword[row + w][col] = letter;
        }
    }
}

// recombine split crosswordItem row arrays back into row strings
function merge(crossword) {
    let board = [];
    if (Array.isArray(crossword[0])) {
        for (let row = 0; row < crossword.length; row++) {
            board.push(crossword[row].join(''));
        }
    } else {
        board = crossword;
    }
    return board;
}

// Complete the crosswordPuzzle function below.
function crosswordPuzzle(crossword, hints) {
    if (hints.length === 0) return crossword;
    let word = hints.pop();
    let slot = check(crossword, word);
    // check(crossword, word).forEach((slot) => did not work, using forloop
    for (let s = 0; s < slot.length; s++) {
        writePuzzle(crossword, word, slot[s]);
        let board = crosswordPuzzle(crossword, hints);
        if (board) {
            return merge(board);
        } else {
            writePuzzle(crossword, word, slot[s], '-');        
        }
    }
    hints.push(word);
}

function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

    let crossword = [];

    for (let i = 0; i < 10; i++) {
        const crosswordItem = readLine().split('');
        // string => read only letters, so split row into col array before push
        crossword.push(crosswordItem);
    }

    const words = readLine().split(';');

    const result = crosswordPuzzle(crossword, words);
    ws.write(result.join('\n') + '\n');

    ws.end();
}

