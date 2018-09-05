
let a = [ "AAPL", "100.07", "IBM",  "192.53", "MSFT", "46.70" ];
//let b = [ "IBM", "MSFT" ];

// Increase size of b 10k times and time the script
const _ = require('lodash');
let b = _.fill(Array(10000), 'X');
b.push("IBM", "MSFT");

let c = [];
for (let i = 0; i < a.length; i+=2) {
    let x = a[i] + ',' + a[i+1] + ',' + (b.indexOf(a[i]) > -1 ? 'Y' : 'N'); 
    c.push(x);
}
console.log(c);

