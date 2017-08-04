'use strict';

var bunyan = require('bunyan');
var config = require('config');

var LOGGER; // bunyan rotating-file fails if instantiated more than once

function createLogger () {
    if (!LOGGER) {
        if (process.env.NODE_ENV !== 'local' || !process.env.NODE_ENV) {
            if (config.logger.streams)
                config.logger.streams.push({
                    level: 'debug',
                    stream: process.stdout
                });
        }
        LOGGER = bunyan.createLogger(config.logger);
    }
    return LOGGER;
}

module.exports = createLogger;
