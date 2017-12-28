let docstore = require('cs-sports-core').docstore();

module.exports = function (season) {
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
