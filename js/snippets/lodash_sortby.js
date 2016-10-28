var _ = require('lodash');
var fs = require('fs');

///var data = JSON.parse(fs.readFileSync(process.argv[1] + 'on').toString());
var title;
var out;

////out = _.cloneDeep(data);

//out.races = _.sortBy(out.races, ['reportingUnits.0.statePostal', 'seatName']);
//out.races = _.orderBy(out.races, ['reportingUnits.0.statePostal', 'seatName'], ['asc', 'desc']);

//out.races = _.sortBy(out.races, 'raceID');  // string-number sorted by first digit
//out.races = _.sortBy(out.races, (o) => { return parseInt(o.raceID); });
////out.races = _.orderBy(out.races, (o) => { return parseInt(o.raceID); }, 'desc');

////console.log(JSON.stringify(out, null, 4));


var polls = [
    {
        ranking: "1",
        name: "Alabama",
        record: "8-0",
        points: "1599",
        ranking_previous: "1"
    },
    {
        ranking: "6",
        name: "Baylor",
        record: "7-1",
        points: "1194",
        ranking_previous: "8"
    },
    {
        ranking: "6",
        name: "Nebraska",
        record: "7-0",
        points: "1194",
        ranking_previous: "9"
    },
    {
        ranking: "10",
        name: "Texas A&M",
        record: "6-1",
        points: "979",
        ranking_previous: "6"
    }
];

//var order = _.orderBy(polls, ['points', 'record'], ['desc', 'desc']); // bad string order

// following is just wrong way
/*
var order = _.orderBy(polls, (p) => {
                return [ parseInt(p.points), parseInt(p.record.split('-')[0]) ];
            }, ['desc', 'desc']);
*/

var order = _.orderBy(polls, [
                (p) => { return parseInt(p.points); },
                (p) => { return parseInt(p.record.split('-')[0]); },
                (p) => { return parseInt(p.record.split('-')[1]); },
            ], ['desc', 'desc', 'asc']);
console.log(order);
