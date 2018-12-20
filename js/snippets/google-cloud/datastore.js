// npm install --save @google-cloud/datastore
const Datastore = require('@google-cloud/datastore');

let _ = require('lodash'),
    format = require('string-format'),
    moment = require('moment'),
    msgpack = require('msgpack'),
    path = require('path'),
    snappy = require('snappy'),
    xxhash = require('xxhash');

// https://github.com/GoogleCloudPlatform/nodejs-getting-started/blob/master/2-structured-data/books/model-datastore.js#L42
function fromDatastore (obj) {
    obj.name = obj[Datastore.KEY].name;
    return obj;
}

// https://github.com/GoogleCloudPlatform/nodejs-getting-started/blob/master/2-structured-data/books/model-datastore.js#L70
function toDatastore (obj, nonIndexed) {
    nonIndexed = nonIndexed || [];
    const results = [];
    Object.keys(obj).forEach((k) => {
        if (obj[k] === undefined) {
            return;
        }
        results.push({
            name: k,
            value: obj[k],
            excludeFromIndexes: nonIndexed.indexOf(k) !== -1
        });
    });
    return results;
}

// https://github.com/GoogleCloudPlatform/nodejs-getting-started/blob/master/2-structured-data/books/model-datastore.js#L91
let listKeys = (ds, kind, limit, token, callback) => {
    let query = ds.createQuery([kind])
    if (limit > 0)
        query = query.limit(limit);
    ds.runQuery(query, (err, entities, nextQuery) => {
        if (err) {
            console.log('\nFailed to run Keys query');
            return;
        }
        if (entities.length === 0) {
            console.log(format('\nNo Keys found for {}', kind))
            return;
        }
        console.log(format('\n{}:', kind))
        _.forEach(entities.map(fromDatastore), (e) => {
            if (!_.startsWith(e.name, '__'))
                console.log(format('  {}', e.name));
        });
        if (limit < 0) {
            console.log(format('\n{} contains {} items', kind, entities.length))
        }
    });
}

let listKinds = (ds, limit) => {
    let query = ds.createQuery(['__Stat_Kind__']).order('kind_name');
    ds.runQuery(query, (err, kinds, nextQuery) => {
        if (err) {
            console.log('\nFailed to run Kinds query');
            return;
        }
        if (kinds.length === 0) {
            console.log(format('\nNo Kinds found!'));
            return;
        }
        _.forEach(kinds, (k) => {
            console.log(format('\nKind: {}\n  Count: {}\n  Bytes: {}', k.kind_name, k.count, k.bytes));
            listKeys(ds, k.kind_name, limit);
        });
    });
}

// does not produce same results as Go "github.com/cespare/xxhash"
let getNameKey = (kind, id) => {
    hash = xxhash.hash64(id, 8, 'hex');
    return ds.key([kind, hash + id]);
}

// https://github.com/GoogleCloudPlatform/nodejs-getting-started/blob/master/2-structured-data/books/model-datastore.js#L140
let readKey = (ds, kind, id, value, hash=false) => {
    let key = hash ? getNameKey(kind, id) : ds.key([kind, id]);
    ds.get(key, (err, entity) => {
        if (!err && !entity) {
            let prefix = hash ? 'Hashed ' : '';
            console.log(format('\n{}Entity not found: {}', prefix, id));
            if (!hash) readKey(ds, kind, id, value, hash=true);
            return;
        }
        console.log(entity);
        if (value) {
            snappy.uncompress(entity.Value, { asBuffer: true }, (err, data) => {
                console.log('Value:', msgpack.unpack(data));
            });
        }
    });
}

// https://github.com/GoogleCloudPlatform/nodejs-getting-started/blob/master/2-structured-data/books/model-datastore.js#L157
let deleteKey = (ds, kind, id) => {
    const key = ds.key([kind, id]);
    ds.delete(key);
}

// https://github.com/GoogleCloudPlatform/nodejs-getting-started/blob/master/2-structured-data/books/model-datastore.js#L116
let writeKey = (ds, kind, id, dataPath) => {
    const key = ds.key([kind, id]);
    const data = require(dataPath);
    snappy.compress(msgpack.pack(data), (err, compressed) => {
        let payload = {
            LastModified: moment().format('YYYY-MM-DD HH:mm:ss'),
            SchemaVersion: '',
            DataType: data.dataType,
            Season: data.season.name || '',
            Sport: data.sport || '',
            League: data.league.alias || '',
            TeamId: data.team.id.toString() || '',
            PlayerId: data.player ? data.player.id : '',
            EventId: data.eventId || '',
            EventDate: data.eventDate || '',
            EventType: data.eventType || '',
            Value: compressed
        };
        const entity = {
            key: key,
            data: toDatastore(payload, _.keys(payload))
        };

        ds.save(entity, err => {
            data.name = entity.key.name;
            if (err) console.log('Error Writing', id, err);
        });
    });
}

let findKeys = (ds, kind, pattern) => {
    let query = ds.createQuery([kind])
    ds.runQuery(query, (err, entities, nextQuery) => {
        if (err) {
            console.log('\nFailed to run Keys query');
            return;
        }
        if (entities.length === 0) {
            console.log(format('\nNo Keys found for {}', kind));
            return;
        }
        let cnt = 0;
        console.log(format('\n{}:', kind));
        _.forEach(entities.map(fromDatastore), (e) => {
            if (e.name.match(pattern)) {
                console.log(format('  {}', e.name));
                cnt++;
            }
        });
        console.log(format('\nFound {} matches for {}', cnt, pattern));
    });
}

let filter = (ds, kind, filter, order) => {
    let query = ds.createQuery([kind]);
    _.forEach(filter.split(','), (f) => {
        let parts = f.match(/^(\w+)(\W+)(\w+)$/);
        query = query.filter(parts[1], parts[2], parts[3]);
    });
    if (order) // order works for TeamId but not Season
        query = query.order(order);
    ds.runQuery(query, (err, entities, nextQuery) => {
        if (err) {
            console.log('\nFailed to run Filter query');
            return;
        }
        if (entities.length === 0) {
            console.log(format('\nNo Keys found for {}', filter));
            return;
        }
        _.forEach(entities.map(fromDatastore), (e) => {
            console.log(format('Entity {}: {} {}/{} ({}) {}', e.DataType, e.Season, e.Sport, e.League, e.LastModified, e.name));
            console.log(format('\tEvent: {}, Team: {}, Player: {}', e.EventId, e.TeamId, e.PlayerId));
        });
    });
}

// MAIN
//console.log(process.argv.length)
if (process.argv.length < 3) {
    console.log('\nUsage:\n\t%s key.json [limit]\n\t%s key.json <action> <params>',
        path.basename(process.argv[0]), path.basename(process.argv[0]));
    console.log(`
    delete <kind> <id>
    filter <kind> <filter1,...,filterN> [<order>]
    find <kind> <pattern>
    list <kind> <count>
    read <kind> <id | id1,..,idN>
    write <kind> <id> <filepath>
    `)
    process.exit(1);
}
// explicitly specifying service_account credentials file
let keyFile = process.argv[2];
process.env['GOOGLE_APPLICATION_CREDENTIALS'] = keyFile;
let keyData = require(keyFile);
let projectID = keyData.project_id;

const ds = new Datastore({
    projectId: projectID
});

if (process.argv.length > 4) {
    switch (process.argv[3]) {
        case "delete":
            deleteKey(ds, process.argv[4], process.argv[5]);
            break;
        case "filter":
            filter(ds, process.argv[4], process.argv[5], process.argv[6]);
            break;
        case "find":
            findKeys(ds, process.argv[4], process.argv[5]);
            break;
        case "list":
            listKeys(ds, process.argv[4], process.argv[5]);
            break;
        case "read":
            readKey(ds, process.argv[4], process.argv[5], process.argv[6]);
            break;
        case "write":
            writeKey(ds, process.argv[4], process.argv[5], process.argv[6]);
            break;
    }
} else {
    let limit = process.argv[3] || 10;
    console.log(format('\nProject: {}\n{}', projectID,
        '-'.repeat(projectID.length + 10)));
        //Array(projectID.length + 10).join('-')));
    listKeys(ds, '__kind__', limit);
    listKinds(ds, limit);
}
