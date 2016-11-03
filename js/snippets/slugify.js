var _ = require('lodash');
var __ = require('underscore');
    __.str = require('underscore.string');

var examples = [
    'Martin Luther King Jr.',
    'Equestrian - Dressage & Eventing',
    'These <3 emoticons ;) don\'t 8-P work',
    'Le garçon wants more     hôtel     space',
    'Shooting >>>----------> arrows at $%#@! TARGETs'
];

examples.forEach((e) => {
    console.log('\n' + e);
    console.log(__.str.slugify(e));
    console.log(_.kebabCase(e));
    console.log(_.snakeCase(e));
});