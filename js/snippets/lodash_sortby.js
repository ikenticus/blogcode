var _ = require('lodash');
var fs = require('fs');

var data = JSON.parse(fs.readFileSync(process.argv[1] + 'on').toString());
var title;
var out;

out = _.cloneDeep(data);

//out.races = _.sortBy(out.races, ['reportingUnits.0.statePostal', 'seatName']);
//out.races = _.orderBy(out.races, ['reportingUnits.0.statePostal', 'seatName'], ['asc', 'desc']);

//out.races = _.sortBy(out.races, 'raceID');  // string-number sorted by first digit
//out.races = _.sortBy(out.races, (o) => { return parseInt(o.raceID); });
out.races = _.orderBy(out.races, (o) => { return parseInt(o.raceID); }, 'desc');

console.log(JSON.stringify(out, null, 4));
