// npm install --save @google-cloud/storage
const {Storage} = require('@google-cloud/storage');

let format = require('string-format'),
    path = require('path');

let list = (bucket) => {
    bucket.getFiles((err, files) => {
        if (err) {
            console.log('Error listing bucket:', err);
        } else {
            files.forEach((f) => {
                //console.log(JSON.stringify(f, null, 4));
                id = f.metadata;
                console.log(format('\nBucket: {}\nName: {}\nContent-Type: {}\nSize: {}\nStorageClass: {}\nCreated: {}',
                    id.bucket, id.name, id.contentType, id.size, id.storageClass, id.timeCreated))
                console.log(format('MD5: {}\nCRC32C: {}\nMediaLink: {}\nACL: {}',
                    id.md5Hash, id.crc32c, id.mediaLink, JSON.stringify(f.parent.storage.acl, null, 4)))
            });
        }
    });
}

let read = (bucket, filename) => {
    let data = '';
    let remoteReadStream = bucket.file(filename).createReadStream();
    remoteReadStream
        .on('data', function (chunk) {
            data += chunk.toString();
            //console.log('CHUNK:', chunk);
        })
        .on('end', function () {
            console.log(data);
        });
}

let write = (bucket, filename) => {
    console.log('TODO');
}

let remove = (bucket, filename) => {
    console.log('TODO');
}

if (process.argv.length < 4) {
    console.log('\nUsage: %s key.json <action> <params>', path.basename(process.argv[0]));
    console.log(`
    create <bucket>
    list <bucket>
    attr <bucket> [<object>]
    read <bucket> <object>
    write <bucket> <object>
    delete <bucket> <object>
    `)
    process.exit(1);
}
// explicitly specifying service_account credentials file
let keyFile = process.argv[2];
const storage = new Storage({
    keyFilename: keyFile
});

let keyData = require(keyFile);
let projectID = keyData.project_id;

let bucket = storage.bucket(process.argv[4]);
switch (process.argv[3]) {
    case "list":
        list(bucket);
        break;
    case "read":
        read(bucket, process.argv[5]);
        break;
    case "write":
        write(bucket, process.argv[5]);
        break;
    case "delete":
        remove(bucket, process.argv[5]);
        break;
}
