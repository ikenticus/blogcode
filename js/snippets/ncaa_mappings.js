var _ = require('lodash');
var fs = require('fs');
var path = require('path');

var cacheFile = path.basename(process.argv[1]) + 'on';
var collection = cacheFile.replace('.json', '_collection.json');

var createTeamCollection = function (teamMap) {
    var teams = [];
    _.forEach(teamMap.teams, (val, key) => {
        teams.push({
            sdi: key,
            usat: val[_.findKey(val, 'abbr')].abbr
        });
    });
    var output = _.clone(teamMap);
    output.teams = teams;
    fs.writeFile(collection, JSON.stringify(output, null, 4), () => {
        process.exit(0);
    });
}

if (fs.existsSync(cacheFile)) {
    fs.access(cacheFile, fs.F_OK, function(err) {
        if (!err) {
            var teamMap = JSON.parse(fs.readFileSync(cacheFile).toString());
            createTeamCollection(teamMap);
        }
    });
}