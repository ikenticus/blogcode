function processData(input) {
    //Enter your code here
    let dates = input.split('\n').map(d => d.split(' ').map(e => parseInt(e, 10)));
    let [[Da, Ma, Ya], [De, Me, Ye]] = dates;

    // Fails for Testcase(s) 3,7 unless we remove the less significant date parts
    /*
    console.log(
        (Ya - Ye > 0) ? 10000 :
        (Ma - Me > 0) ? 500 * (Ma - Me) :
        (Da - De > 0) ? 15 * (Da - De) :
        0    
    );
    */

    // Works but may not be as accurate as datediff functions
    console.log(
        (Ya - Ye > 0) ? 10000 :
        (Ya - Ye >= 0 && Ma - Me > 0) ? 500 * (Ma - Me) :
        (Ya - Ye >= 0 && Ma - Me >= 0 && Da - De > 0) ? 15 * (Da - De) :
        0    
    );
} 

process.stdin.resume();
process.stdin.setEncoding("ascii");
_input = "";
process.stdin.on("data", function (input) {
    _input += input;
});

process.stdin.on("end", function () {
   processData(_input);
});

