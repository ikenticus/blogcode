/*
You are given two arrays of data.
The arrays are simple string arrays.

The first contains stock tickers and their price. The ticker and associated price are adjacent to each other.
For example:
    [ "AAPL", "100.07", "IBM",  "192.53", "MSFT", "46.70" ]

The second array contains a list of stock tickers that are part of a portfolio. A ticker from the first array may or may not be present in the second array.
For example:
    [ "IBM", "MSFT" ]

Write a program that will join the information contained in both arrays and return a new string array.
For example:
 
    [ "AAPL,100.07,N", "IBM,192.53,Y", "MSFT,46.70,Y" ]

where is_owned = Y if the ticker is in the portfolio (is in the second array), N otherwise
*/
 
let a = [ "AAPL", "100.07", "IBM",  "192.53", "MSFT", "46.70" ];
let b = [ "IBM", "MSFT" ];
let c = [];
for (let i = 0; i < a.length; i+=2) {
    let x = a[i] + ',' + a[i+1] + ',' + (b.indexOf(a[i]) > -1 ? 'Y' : 'N'); 
    c.push(x);
}
console.log(c);

// Follow up question from Sara:
// if there any way to make it more efficient to avoid looping through the b array for each item in a?

