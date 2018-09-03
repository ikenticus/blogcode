function processData(input) {
    //Enter your code here
    let inputString = input.split("\n");
    let T = inputString[0];
    inputString.slice(1).forEach((S) => {
        let output = ['', ''];
        for (let c = 0; c < S.length; c++) {
            if (c % 2 === 0) {
                output[0] += S[c]; 
            } else {
                output[1] += S[c]; 
            }
        }
        console.log(output.join(' '));
    });
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

