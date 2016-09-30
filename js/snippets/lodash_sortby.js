var _ = require('lodash');
var fs = require('fs');

var data = JSON.parse(fs.readFileSync(process.argv[1] + 'on').toString());
var title;
var out;

out = _.cloneDeep(data);
//out.races = _.orderBy(out.races, ['reportingUnits.0.statePostal'], ['desc']);
out.races = _.sortBy(out.races, ['reportingUnits.0.statePostal', 'seatName']);
console.log(JSON.stringify(out, null, 4));
