
# pip install --upgrade google-cloud-datastore
from google.cloud import datastore
from datetime import datetime

import json
import msgpack
import os
import re
import snappy   # brew install snappy; pip install python-snappy
import sys
import xxhash

# https://github.com/GoogleCloudPlatform/getting-started-python/blob/504b3d550b551502cfe96f32542c31b232135eff/2-structured-data/bookshelf/model_datastore.py#L31
def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    #entity['id'] = entity.key.id
    return entity

def filter(ds, kind, filter, order=None):
    pattern = re.compile('^(\w+)(\W+)(\w+)$')
    query = ds.query(kind=kind)
    for f in filter.split(','):
        parts = pattern.match(f)
        query.add_filter(*parts.group(1,2,3))
    if order: # order works for TeamId but not Season nor DataType
        query.order = [order]
    entities = query.fetch()
    for e in entities:
        print 'Entity %s: %s %s/%s (%s) %s' % (e['DataType'], e['Season'], e['Sport'], e['League'], e['LastModified'], e.key)
        print '\tEvent: %s, Team: %s, Player: %s' % (e['EventId'], e['TeamId'], e['PlayerId'])

# https://github.com/GoogleCloudPlatform/getting-started-python/blob/504b3d550b551502cfe96f32542c31b232135eff/2-structured-data/bookshelf/model_datastore.py#L96
def delete_key(ds, kind, id, unused):
    key = ds.key(kind, id)
    ds.delete(key)

def find_keys(ds, kind, filter, order):
    print 'TODO: cannot find until id can be extracted from key'

def list_keys(ds, kind, limit, order=None):
    query = ds.query(kind=kind)
    if order:
        query.order = [order]
    entities = query.fetch(limit=limit)
    found = False
    for e in entities:
        found = True
        print e.key
        '''
        if not e['kind_name'].startsWith('__'):
            print '  %s' % e['kind_name']
        '''
    if not found:
        print '\nNo Entities found!'
    '''
    if limit < 0:
        print '\n%s contains %d items' % (kind, len(entities))
    '''

def list_kinds(ds, limit):
    query = ds.query(kind='__Stat_Kind__', order=['kind_name'])
    kinds = query.fetch(limit=limit)
    found = False
    for k in kinds:
        found = True
        print '\nKind: %s\n  Count: %d\n  Bytes: %d' % (k['kind_name'], k['count'], k['bytes'])
        list_keys(ds, k['kind_name'], limit);
    if not found:
        print '\nNo Kinds found!'

def get_hashed_key(kind, id):
    hash = xxhash.xxh64(id).intdigest()
    return ds.key(kind, '%d%s' % (hash, id))

# https://github.com/GoogleCloudPlatform/getting-started-python/blob/504b3d550b551502cfe96f32542c31b232135eff/2-structured-data/bookshelf/model_datastore.py#L68
def read_key(ds, kind, id, value=False):
    key = ds.key(kind, id)
    results = ds.get(key)
    if not results:
        print '\nEntity not found: %s' % key
        key = get_hashed_key(kind, id)
        results = ds.get(key)
        if not results:
            print '\nHashed entity not found: %s' % key
            return
    entity = from_datastore(results)

    for k in sorted(entity.keys()):
        if k != 'Value':
            print '%s: %s' % (k, entity[k])

    if value:
        data = snappy.decompress(entity['Value'])
        print 'Value:', msgpack.unpackb(data)

# https://github.com/GoogleCloudPlatform/getting-started-python/blob/504b3d550b551502cfe96f32542c31b232135eff/2-structured-data/bookshelf/model_datastore.py#L76
def write_key(ds, kind, id, data_path):
    key = ds.key(kind, id)
    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=['Value'])

    with open(data_path) as f:
        data = json.load(f)

    payload = {
        'LastModified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'SchemaVersion': '',
        'DataType': data['dataType'],
        'Season': data['season']['name'],
        'Sport': data['sport'] if 'sport' in data else '',
        'League': data['league']['alias'],
        'TeamId': str(data['team']['id']),
        'PlayerId': data['player']['id'] if 'player' in data else '',
        'EventId': data['eventId'] if 'eventId' in data else '',
        'EventDate': data['eventDate'] if 'eventDate' in data else '',
        'EventType': data['eventType'] if 'eventType' in data else '',
        'Value': snappy.compress(msgpack.packb(data))
    }
    print payload

    entity.update(payload)
    ds.put(entity)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '''\nUsage:\n\t%s key.json [limit]\n\t%s key.json <action> <params>

        delete <kind> <id>
        filter <kind> <filter1,...,filterN> [<order>]
        find <kind> <pattern>
        list <kind> <count>
        read <kind> <id | id1,..,idN>
        write <kind> <id> <filepath>
        ''' % (os.path.basename(sys.argv[0]), os.path.basename(sys.argv[0]))
        sys.exit(1);

    key_file = sys.argv[1]
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file
    with open(key_file) as f:
        creds = json.load(f)
    project_id = creds['project_id']
    ds = datastore.Client(project_id)

    if len(sys.argv) > 3:
        action = sys.argv[2]
        kind = sys.argv[3]
        id = sys.argv[4]
        switcher = {
            'delete': delete_key,
            'filter': filter,
            'find': find_keys,
            'list': list_keys,
            'read': read_key,
            'write': write_key
        }
        func = switcher.get(action, 'Invalid Action')
        extra = '' if len(sys.argv) < 6 else sys.argv[5]
        func(ds, kind, id, extra)
    else:
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10;
        print '\nProject: %s\n%s' % (project_id, '-' * (len(project_id) + 10))
        list_keys(ds, '__kind__', limit)
        list_kinds(ds, limit)
