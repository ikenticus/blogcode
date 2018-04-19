var AWS = require('aws-sdk');
AWS.config.update({
    region: process.env.S3_REGION,
    accessKeyId: process.env.S3_ACCESS,
    secretAccessKey: process.env.S3_SECRET
});
var s3 = new AWS.S3();

var params = { 
    Bucket: process.env.S3_BUCKET,
    Delimiter: '/'
    // Prefix: 's/5469b2f5b4292d22522e84e0/ms.files/'
}

s3.listObjects(params, (err, files) => {
    if (err) {
        console.log('ERROR', err);
    } else {
        files.Contents.forEach((f) => {
            var data = '';
            var params = {Bucket: process.env.S3_BUCKET, Key: f.Key};
            var remoteReadStream = s3.getObject(params).createReadStream()
            remoteReadStream
                .on('data', function (chunk) {
                    data += chunk.toString();
                    //console.log('CHUNK:', chunk);
                })
                .on('end', function () {
                    console.log('\nFILE:', f.Key)
                    console.log(data)
                });
        });
    }
});
