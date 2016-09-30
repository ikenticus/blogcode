var _ = require('lodash');
var fs = require('fs');

var data = JSON.parse(fs.readFileSync(process.argv[1] + 'on').toString());
var title;
var out;

title = '\n===== President =====\n';
out = _.filter(data.races, { raceTypeID: 'G', officeID: 'P' });
//console.log(title, out);

title = '\n===== Senate =====\n';
out = _.filter(data.races, { raceTypeID: 'G', officeID: 'S' });
//console.log(title, out);

title = '\n===== President, CA =====\n';
out = _.cloneDeep(data);
_.forEach(out.races, (race) => {
    race.reportingUnits = _.filter(race.reportingUnits, { statePostal: 'CA' });
});
out.races = _.filter(out.races, { raceTypeID: 'G', officeID: 'P' });
out.races = _.filter(out.races, (r) => { return r.reportingUnits.length > 0; });
//console.log(title, out);
//console.log(title, JSON.stringify(out, null, 4));

title = '\n===== President, CA, national =====\n';
out = _.cloneDeep(data);
_.forEach(out.races, (race) => {
    race.reportingUnits = _.filter(race.reportingUnits, { statePostal: 'CA', level: 'state' });
});
out.races = _.filter(out.races, { raceTypeID: 'G', officeID: 'P' });
out.races = _.filter(out.races, (r) => { return r.reportingUnits.length > 0; });
//console.log(title, JSON.stringify(out, null, 4));

title = '\n===== President, CA, county =====\n';
out = _.cloneDeep(data);
out.races = _.filter(out.races, { raceTypeID: 'G', officeID: 'P' });
_.forEach(out.races, (race) => {
    race.reportingUnits = _.filter(race.reportingUnits, { statePostal: 'CA', level: 'subunit' });
});
out.races = _.filter(out.races, (r) => { return r.reportingUnits.length > 0; });
//console.log(title, JSON.stringify(out, null, 4));

title = '\n===== Senator, NY, county =====\n';
out = _.cloneDeep(data);
out.races = _.filter(out.races, { raceTypeID: 'G', officeID: 'S' });
_.forEach(out.races, (race) => {
    race.reportingUnits = _.filter(race.reportingUnits, { statePostal: 'NY', level: 'subunit' });
    _.forEach(race.reportingUnits, (ru) => {
        ru.incumbent = _.filter(ru.candidates, 'incumbent')[0].last;
    });
});
out.races = _.filter(out.races, (r) => { return r.reportingUnits.length > 0; });
console.log(title, JSON.stringify(out, null, 4));

/*
var url = 'http://api.ap.org/v2/elections/2016-11-08?apikey=LZwNnR5WuvyahrgNEnxpsPVf1z2pKQZG&format=json&test=true&OfficeID=P,S&raceTypeID=G&level=RU&statePostal=NY,CA';
var request = require('request');
request.get({url}, (err, res, body) => {
    if (!err) {
        var raw = JSON.parse(body);
        var fix = _.cloneDeep(raw);
        fix.races = _.filter(fix.races, { raceTypeID: 'G', officeID: 'P' });
        _.forEach(fix.races, (race) => {
            race.reportingUnits = _.filter(race.reportingUnits, { statePostal: 'CA', level: 'state' });
        });
        fix.races = _.filter(fix.races, (r) => { return r.reportingUnits.length > 0; });
        console.log(JSON.stringify(fix, null, 4));
    }
});
*/