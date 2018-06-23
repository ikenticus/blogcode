'use strict';

var fs = require('fs');
var refparser = require('json-schema-ref-parser');

var contents = fs.readFileSync("test_data/image5.json");
var mySchema = JSON.parse(contents);

refparser.dereference(mySchema, function(err, schema) {
    if (err) {
        console.error(err);
    } else {
        console.log(JSON.stringify(schema, null, 4));
    }
});
