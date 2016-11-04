var _ = require('lodash');
var fs = require('fs');

var data = JSON.parse(fs.readFileSync(process.argv[1] + 'on').toString());

console.log('\nLIST forEach');
console.log('===== basic');
data.feed['league-content']['season-content']['conference-content'].forEach(function(c) {
	console.log(c.conference.id);
	c['division-content'].forEach(function(d) {
		console.log(d.division.id);
	});
});
console.log('===== lodash');
_.forEach(data.feed['league-content']['season-content']['conference-content'], (c) => {
	console.log(c.conference.id);
	_.forEach(c['division-content'], (d) => {
		console.log(d.division.id);
	});
});

console.log('\nDICT forEach');
console.log('===== basic');
var name = data.feed['league-content'].league.name[1];
Object.keys(name).forEach(function(m) {
	console.log(m, name[m]);
});
console.log('===== lodash');
_.forEach(name, (n, m) => {
	console.log(m, n);
});

/*
function bindRoutes (handlers, api) {
    // basic
    Object.keys(handlers).forEach(function bindRoute(path) {
        logger.info('Binding path:' + path);
        var routes = handlers[path];
        Object.keys(routes).forEach(function bindRouteMethod(method) {
            api[method](path, routes[method]);
        });
    });
    // lodash
    _.forEach(handlers, (routes, path) => {
        logger.info('Binding path:' + path);
        _.forEach(routes, (routeMethod, method) => {
            api[method](path, routeMethod);
        });
    });
}
*/

console.log('\nMAP');
var out = {};
data = { one: 1, two: 2, three: 3, four: 4, five: 5 };
console.log('===== basic');
Object.keys(data).map(function(key) {
    if (data[key] % 2) out[key] = data[key] * 10;
});
console.log(out);
console.log('===== lodash');
_.map(data, (key) => {
    if (data[key] % 2) out[key] = data[key] * 10;
});
console.log(out);


console.log('\n\n\n\n\n\n\n\n\nSTART')
data = {
    //ELEM: [ 1, 2, 3, 4 ],
    //MIDDLE: [ 5, 6, 7, 8 ],
    HIGH: null,
    COLLEGE: {
        Freshman: {
            Math: { Calculus: [ 'AB', 'BC' ] }
        },
        Sophomore: {
            Math: {
                Algebra: [ 'I', 'II' ],
                Geometry: [ 1, 2, 3, 4 ],
                Trigonometry: [ 1, 2, 3 ]
            }
        },
        Junior: {},
        Senior: {}
    }
}
var orig = _.cloneDeep(data);
console.log('===== orig');
console.log(orig);

console.log('\n\n\nCLONE equal');
var equal = orig;
console.log('-- COLLEGE -> HIGH');
equal.HIGH = equal.COLLEGE
console.log('===== equal');
console.log(equal);
console.log('===== orig');
console.log(orig);
console.log('-- Sophomore -> Junior');
equal.COLLEGE.Junior = equal.COLLEGE.Sophomore;
console.log('===== equal');
console.log(equal);
console.log('===== orig');
console.log(orig);
console.log('-- delete College Sophomore Geometry');
delete equal.COLLEGE.Sophomore.Math.Geometry;
console.log('===== equal');
console.log(JSON.stringify(equal, null, 4));
console.log('===== orig');
console.log(JSON.stringify(orig, null, 4));


console.log('\n\n\nCLONE shallow');
orig = _.cloneDeep(data);
console.log('-- COLLEGE -> HIGH');
var shallow = _.clone(orig);
shallow.HIGH = _.clone(shallow.COLLEGE);
console.log('===== shallow');
console.log(shallow);
console.log('===== orig');
console.log(orig);
console.log('-- Sophomore -> Junior');
shallow.COLLEGE.Junior = _.clone(shallow.COLLEGE.Sophomore);
console.log('===== shallow');
console.log(shallow);
console.log('===== orig');
console.log(orig);
console.log('-- delete College Sophomore Geometry');
delete shallow.COLLEGE.Sophomore.Math.Geometry;
console.log('===== shallow');
console.log(JSON.stringify(shallow, null, 4));
console.log('===== orig');
console.log(JSON.stringify(orig, null, 4));


console.log('\n\n\nCLONE deep');
orig = _.cloneDeep(data);
console.log('-- COLLEGE -> HIGH');
var deep = _.cloneDeep(orig);
deep.HIGH = _.cloneDeep(deep.COLLEGE);
console.log('===== deep');
console.log(deep);
console.log('===== orig');
console.log(orig);
console.log('-- Sophomore -> Junior');
deep.COLLEGE.Junior = _.cloneDeep(deep.COLLEGE.Sophomore);
console.log('===== deep');
console.log(deep);
console.log('===== orig');
console.log(orig);
console.log('-- delete College Sophomore Geometry');
delete deep.COLLEGE.Sophomore.Math.Geometry;
console.log('===== deep');
console.log(JSON.stringify(shallow, null, 4));
console.log('===== orig');
console.log(JSON.stringify(orig, null, 4));


