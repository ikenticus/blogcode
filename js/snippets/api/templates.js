'use strict';

var fs = require('fs');
var format = require('string-format');
var handlebars = require('handlebars');
require('handlebars-helpers')();

var logger = require('../lib/logger.js')();

var applyTemplate = function (templates, view) {
    var applied = false;
    var output = view;
    templates.forEach(function(templateName) {
        var templatePath = format('templates/{}.hbs', templateName.join('_'));
        if (fs.existsSync(templatePath)) {
            if (applied !== true) {
                logger.info('Applying template: ' + templatePath);
                var source = fs.readFileSync(templatePath).toString();
                var template = handlebars.compile(source);

                /*
                // register one partial, switch to loop if adding more later
                var partialName = 'schedule';
                var partialPath = format('templates/partials/{}.hbs', partialName);
                var partial = fs.readFileSync(partialPath).toString();
                handlebars.registerPartial(partialName, partial);
                */
                fs.readdirSync('templates/partials')
                    .forEach(function loadPartial(partialFile) {
                        //logger.info('Loading partial: ' + partialFile);
                        var partialName = partialFile.replace(/\.hbs$/, '');
                        var partialPath = format('templates/partials/{}', partialFile);
                        var partialJson = fs.readFileSync(partialPath).toString();
                        handlebars.registerPartial(partialName, partialJson);
                    }
                );

                // Removing Try/Catch to allow 503 errors to appear on Akamai
                //try {
                    output = JSON.parse(template(view));
                //} catch (err) {
                //    view.error = format('There was a problem applying template: {}', templatePath);
                //    output = view;
                //}
                applied = true;
            }
        }
    });
    return output;
};

var buildTemplates = function (params) {
    // templates fallback from right to left, value then key
    // i.e. universal_olympics_2012
    //      universal_olympics_season
    //      universal_sport_2012
    //      universal_sport_season
    var templates = [];
    var values = Object.keys(params).map(function(key) {
        return params[key].toLowerCase();
    });
    var keys = Object.keys(params);
    for (var t = 0; t < Math.pow(2, keys.length); t++) {
        templates.push(values.slice());
    }
    for (var p = 0; p < keys.length; p++) {
        var index = keys.length - p - 1;
        for (var i = 0; i < Math.pow(2, index); i++) {
            for (var c = 0; c < Math.pow(2, p); c++) {
                var order = i * Math.pow(2, p + 1) + c + Math.pow(2, p);
                templates[order][index] = keys[index];
            }
        }
    }
    return templates;
};

module.exports = {
    apply: applyTemplate,
    build: buildTemplates
};
