'use strict';
if (process.env.ENVIRONMENT) require('newrelic');

let _ = require('lodash'),
    config = require('config'),
    express = require('express'),
    format = require('string-format'),
    fs = require('fs'),
    path = require('path'),
    restify = require('restify'),
    url = require('url');

let staticDocServer = express.static(path.dirname(require.resolve('swagger-ui')));

let logger = require('cs-sports-core').logger();

// only reason to bind routes like this instead of actually binding is so that the views can be tested
// without having to mock out the api
function bindRoutes (handlers, api) {
    _.forEach(handlers, (routes, path) => {
        logger.info('Binding path:' + path);
        _.forEach(routes, (routeMethod, method) => {
            api[method]({ path: path, flags: 'i' }, routeMethod);
        });
    });
}

function swaggerAnchor (prefix) {
    // swagger-ui 2.2.6 used #/SportsConsumer_Service.svc
    var anchor = format('#/Sports{}_{}', _.upperFirst(prefix[1].slice(6)),
        config.legacy.services[prefix[2]] || _.upperFirst(prefix[2]));
    // swagger-ui 2.2.9 switched to #/SportsConsumer32Service46svc
    anchor = anchor.slice(0, 2)
           + anchor.slice(2).replace('_', ' ')
                   .replace(/[^A-Za-z0-9]/g, (w) => { return w.charCodeAt(0); });
    return anchor;
}

function createServer () {
    var server = restify.createServer({});
    server.use(restify.plugins.acceptParser(server.acceptable));
    server.use(restify.plugins.jsonp());
    server.use(restify.plugins.queryParser({'mapParams':false}));
    server.use(restify.plugins.bodyParser());
    server.use(restify.plugins.requestLogger());

    // GraphQL
    const {graphqlRestify, graphiqlRestify} = require('graphql-server-restify');
    const schema = require('./schema');
    server.post('/graphql', graphqlRestify({schema}));
    server.get('/graphql', graphqlRestify({schema}));
    server.get('/graphiql', graphiqlRestify({ endpointURL: '/graphql' }));
 
    server.on('uncaughtException', function(req, res, route, error) {
        logger.error(error);
        return res.send(500, error);
    });

    process.on('uncaughtException', function(error) {
        logger.error(error);
    });

    /*
    server.use(function requireConsumerParam(req, res, next) {
        if (req.url.indexOf('help') > -1 || req.url.indexOf('api-docs') > -1)  return next(); // don't require consumer params for swagger
        if(!req.params.consumer) return next(new restify.InvalidArgumentError('Consumer not passed in'));
        return next();
    });
    */

    server.get(/(\/\w+)*\/api-docs\/(.+)?$/, function (req, res, next) {
        var swaggerPath = format('./swagger/{}', req.params[1]);
        var swaggerJson = fs.readFileSync(swaggerPath).toString();
        res.send(JSON.parse(swaggerJson));
        next();
    });

    server.get(/(\/[\w\/\.]+)*\/help(\/.*)?$/, function(req, res, next) {
        var startUrl = url.parse(req.url, true);
        var redirUrl = url.format(startUrl);
        if (req.params[1] === undefined || !req.query.url) {
            if (req.params[1] === undefined) {
                startUrl.pathname += '/'; // express static wants a trailing slash
            }
            if (!req.query.url) {
                var anchor = '';
                var prefix = req.params[0] || '';
                if (prefix.toLowerCase().indexOf('/sports') > -1) {
                    // for legacy /Sports(Data|Hub|Tools) help
                    if (prefix.indexOf('.svc') > 0) {
                        prefix = prefix.toLowerCase().split('/');
                        startUrl.query.url = format('/api-docs/{}.json', prefix[1]);
                        anchor = swaggerAnchor(prefix);
                    } else {
                        startUrl.query.url = '/api-docs/' + prefix.toLowerCase().slice(1) + '.json';
                    }
                } else {
                    startUrl.query.url = prefix + '/api-docs/swagger.json';
                }
                startUrl.search = '';   // format only joins query when search is empty
                redirUrl = url.format(startUrl) + anchor;
            }
            res.redirect(302, (redirUrl || req.url), next);
        }
        req.url = redirUrl.substr(redirUrl.indexOf('/help') + '/help'.length); // fix pathing
        return staticDocServer(req, res, next);
    });

    fs.readdirSync('./views').forEach(function loadView(viewFile) {
        logger.info('Loading route: ' + viewFile);
        bindRoutes(require('./views/' + viewFile), server);
    });

    return server;
}

var server = createServer(logger);
server.listen(3000);
