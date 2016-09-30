var _ = require('lodash');
var fs = require('fs');

var data = JSON.parse(fs.readFileSync(process.argv[1] + 'on').toString());

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


