var _ = require('lodash');

var AWS = require('aws-sdk');
AWS.config.update({
    region: process.env.REGION,
    accessKeyId: process.env.ACCESS,
    secretAccessKey: process.env.SECRET
});
var ddb = new AWS.DynamoDB();

var params = {
    //ExclusiveStartTableName: 'STRING_VALUE',
    //Limit: 'NUMBER_VALUE'
};

var listTables = function (params) {
    ddb.listTables(params, function(err, data) {
        if (err) return console.log(err, err.stack);
        _.forEach(data.TableNames, t => {
            console.log('Describing', t);
            descTable({TableName: t});
        });
    });
}

var descTable = function (params) {
    ddb.describeTable(params, function(err, data) {
        if (err) return console.log(err, err.stack);
        console.log(data);
    });
}

listTables(params);

