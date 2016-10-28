var _ = require('lodash');
var config = require('config');
var fs = require('fs');
var moment = require('moment');
var path = require('path');
var request = require('request');

var cacheFile = path.basename(process.argv[1]) + 'on';
var mappings = cacheFile.replace('.json', '_mappings.json');

var teamsData;

var _updateTeams = function (league, team, teams) {
    if (team['season-details'].tier == 1) {
        var subsport = _.find(league.name, { type: 'nick' })._;
            subsport = (subsport === 'WNCAAB') ? 'NCAAW' : subsport;
        var abbr = _.find(team.name, { type: 'short' })._;

        if (_.keys(teams).indexOf(abbr) < 0) teams[abbr] = {};
        teams[abbr][subsport] = {
            id: team.id,
            abbr: abbr,
            school: _.find(team.name, { type: 'first' })._,
            mascot: _.find(team.name, { type: 'nick' })._
        };
    }
};

var createTeamMap = function (teamsData) {
    var teams = {};
    _.forEach(_.sortBy(teamsData, 'id'), (league) => {
        var conferences = league.sports.feed['league-content']['season-content']['conference-content'];
        _.forEach(conferences, (conference) => {
            if (_.keys(conference).indexOf('division-content') > -1) {
                _.forEach(conference['division-content'], (division) => {
                    _.forEach(division['team-content'], (team) => {
                        _updateTeams(league.sports.feed['league-content'].league, team.team, teams);
                    });
                });
            } else if (_.keys(conference).indexOf('team-content') > -1) {
                if (!_.isArray(conference['team-content']))
                    conference['team-content'] = [conference['team-content']];
                _.forEach(conference['team-content'], (team) => {
                    _updateTeams(league.sports.feed['league-content'].league, team.team, teams);
                });
            }
        });
    });
    var output = { teams: {} };
    _.keys(teams).sort().forEach((key) => {
        output.teams[key] = teams[key];
    });
    fs.writeFile(mappings, JSON.stringify(output, null, 4), () => {
        process.exit(0);
    });
}

if (fs.existsSync(cacheFile)) {
    fs.access(cacheFile, fs.F_OK, function(err) {
        if (!err) {
            teamsData = JSON.parse(fs.readFileSync(cacheFile).toString());
            createTeamMap(teamsData);
        }
    });
} else {
    request.get({
        url: 'http://localhost:3000/feed/search',
        //url: config.post + '/feed/search',
        qs: {
            _limit: '5',
            type: 'teams',
            subcategory: 'sdi',
            subsport: '~NCAA_',
            season: moment().format('Y')
        }
    }, (err, res, body) => {
        if (!err) {
            teamsData = JSON.parse(body);
            fs.writeFile(cacheFile, JSON.stringify(teamsData, null, 4), (err) => {
                if (!err) createTeamMap(teamsData);
            });
        }
    });
}
