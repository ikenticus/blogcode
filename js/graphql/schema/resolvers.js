let _ = require('lodash');

let docstore = require('cs-sports-core').docstore();
let resolvers = require('cs-sports-show-olympics').resolvers;

const links = [
    {
        id: 1,
        url: 'http://graphql.org/',
        description: 'The Best Query Language'
    },
    {
        id: 2,
        url: 'http://dev.apollodata.com',
        description: 'Awesome GraphQL Client'
    },
];

var whichLink = function (id) {
    return _.filter(links, { id: parseInt(id) });
};

let sports = function (season) {
    return new Promise((resolve, reject) => {
        let docId = 'feed_usat_olympics_sports_' + season;
        docstore.get(docId)
            .then(function(result) {
                if (result[docId])
                    resolve(result[docId].feed);
            })
            .catch(function(error) {
                reject([{error: error}]);
            });
    });
};

module.exports = {
    Query: {
        allLinks: () => links,
        whichLink: (root, { id }) => whichLink(id),
        chooseLink: (root, { id }) => {
            return _.filter(links, { id: parseInt(id) });
        },

        sports: (root, { season }) => resolvers.sports(season)
    }
};
