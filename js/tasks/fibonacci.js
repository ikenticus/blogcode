/*
    Task: Fibonacci
*/
let _ = require('lodash'),
    format = require('string-format'),
    path = require('path');

function usage() {
    console.log(format('Calculate the Nth Fibonacci number\nUsage: {} <n>', path.basename(process.argv[1])));
}

function fibonacci(n) {
    f = [0, 1];
    for (let i = 2; i <= n; i++) {
        f.push(f[i-2] + f[i-1]);
    }
    //console.log(f);
    return f[n];
}

// main
let SEQ = [ 0, 1 ];
if (process.argv.length === 2) {
    usage();
    process.exit(1);
} else if (parseInt(process.argv[2]) <= 1) {
    console.log(format('F({}) = {}', process.argv[2], process.argv[2]));
    if (parseInt(process.argv[2]) < 1)
        SEQ = SEQ.splice(0, 1);
} else {
    let NUM = parseInt(process.argv[2]);
    if (NUM > 1) {
        _.range(2, NUM+1).forEach((i) => {
            SEQ.push(SEQ[i-1] + SEQ[i-2]);
        });
    }
    SIZE = SEQ.length - 1;
    console.log(format('F({}) = {}', NUM, SEQ[SIZE]));
}
console.log('Sequence:', SEQ);
