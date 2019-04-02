let fs = require('fs');
let parseString = require('xml2js').parseString;
 
fs.readFile(process.argv[2], 'utf8', function(err, input) {
    //console.log(input);
    parseString(input, function (err, output) {
        if (err) {
            console.log(err);
        } else {
            console.log(JSON.stringify(output, null, 4));
        }
    });
});

