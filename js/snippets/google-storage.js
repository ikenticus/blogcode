
const Storage = require('@google-cloud/storage');
// authenticate using ONE (not ALL) of the following methods:
 
// setting environment variable GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json
const storage = new Storage();
 
/*
// explicitly specifying service_account credentials file
const storage = new Storage({
    keyFilename: '/path/to/service_account.json'
});

// passing in credentials as JSON
const storage = new Storage({
    credentials: {
        type: "service_account",
        project_id: process.env.PROJECT_ID,
        private_key_id: process.env.PRIVATE_KEY_ID,
        private_key: process.env.PRIVATE_KEY
        client_email: "{USER}@{PROJECT}.iam.gserviceaccount.com",
        client_id: process.env.CLIENT_ID
        auth_uri: "https://accounts.google.com/o/oauth2/auth",
        token_uri: "https://accounts.google.com/o/oauth2/token",
        auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs",
        client_x509_cert_url: "https://www.googleapis.com/robot/v1/metadata/x509/{USER}%40{PROJECT}.iam.gserviceaccount.com"
    }
});
*/

var bucket = storage.bucket(process.env.BUCKET_NAME);
bucket.getFiles(function(err, files) {
    if (err) {
        console.log('ERROR', err);
    } else {
        files.forEach((f) => {
            var data = '';
            var remoteReadStream = bucket.file(process.env.BUCKET_FILE).createReadStream();
            remoteReadStream
                .on('data', function (chunk) {
                    data += chunk.toString();
                    //console.log('CHUNK:', chunk);
                })
                .on('end', function () {
                    console.log('\nFILE:', f.name)
                    console.log(data)
                });
        });
    }
});
