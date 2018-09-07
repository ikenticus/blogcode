function processData(input) {
    //Enter your code here

    input.split('\n').splice(1).forEach((n) => {
        let prime = true;
        if (n === '1') { // fixes Testcase 5
            prime = false;
        } else {
            let root = Math.sqrt(n);
            // i < root; fails for Testcase 9; use i <= root
            for (let i = 2; i <= root; i++) {
                if (n % i === 0)
                    prime = false;
            }            
        }
        console.log(prime ? 'Prime' : 'Not prime');
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

