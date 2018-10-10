'''
    dns-importer: read in csv file and upload
'''
import csv
import os
import sys
from ns1 import NS1, Config
from twisted.internet import defer, reactor

# Increase timeout if too many twisted ConnectionLost
REACTOR_TIMEOUT = 5

# load default config from ~/.nsone (see nsone.sample)
config = Config()
config.loadFromFile(Config.DEFAULT_CONFIG_FILE)

'''
# OR generate default with api key AND adjust config
config.createFromAPIKey('AbCdEfGhiJKlMnOpQrSt')
config['transport'] = 'twisted'
config['verbosity'] = 5
'''

api = NS1(config=config)


def fix_data(r):
    ''' fix_data is used to reshape the data according to the type '''
    if r['Type'] == 'MX':
        data = r['Data'].split(' ')
        return [[ int(data[0]), ' '.join(data[1:]) ]]
    else:
        return r['Data']

@defer.inlineCallbacks
def add_record(zone, r):
    ''' asynchronous attempt to add record '''
    if r['Name'] == '@':
        rec = yield getattr(zone, 'add_' + r['Type'])(r['Zone'], fix_data(r), ttl=r['TTL'])
    else:
        rec = yield getattr(zone, 'add_' + r['Type'])(r['Name'], fix_data(r), ttl=r['TTL'])
    defer.returnValue(rec)

def record_added(record, r):
    ''' callback for add_record '''
    print('SUCCESS Adding %s %s record %s: %s' % (r['Zone'], r['Type'], r['Name'], record))

def record_add_error(failure, r):
    ''' errorback for add_record '''
    print('FAILURE Adding %s %s record %s: %s' % (r['Zone'], r['Type'], r['Name'], failure.value))

@defer.inlineCallbacks
def load_record(zone, r):
    ''' asynchronous attempt to load record '''
    if r['Name'] == '@':
        rec = yield api.loadRecord(r['Zone'], r['Type'])
    else:
        rec = yield zone.loadRecord(r['Name'], r['Type'])
    defer.returnValue(rec)

def record_loaded(record, r):
    ''' callback for load_record '''
    answers = [ ' '.join([ str(a) for a in ra['answer'] ]) for ra in record.answers ]
    if r['Data'] in answers:
        print('SUCCESS Loading %s %s record %s: %s' % (r['Zone'], r['Type'], r['Name'], answers))
    else:
        #print('MISSING %s %s record %s: %s' % (r['Zone'], r['Type'], r['Name'], answers))
        adder = record.addAnswers(fix_data(r))
        adder.addCallback(record_added, r)
        adder.addErrback(record_add_error, r)

def record_load_error(failure, zone, r):
    ''' errorback for load_record '''
    if str(failure.value).endswith('record not found'):
        adder = add_record(zone, r)
        adder.addCallback(record_added, r)
        adder.addErrback(record_add_error, r)
    else :
        print('FAILURE Loading %s %s record %s: %s' % (r['Zone'], r['Type'], r['Name'], failure.value))

@defer.inlineCallbacks
def load_zone(name):
    ''' asynchronous attempt to load zone '''
    zone = yield api.loadZone(name)
    defer.returnValue(zone)

def zone_loaded(zone, name, records):
    ''' callback for load_zone '''
    print('SUCCESS Loading zone %s: %s' % (name, zone))
    for r in records:
        loader = load_record(zone, r)
        loader.addCallback(record_loaded, r)
        loader.addErrback(record_load_error, zone, r)

def zone_error(failure, name):
    ''' errorback for load_zone '''
    print('FAILURE Loading zone %s: %s' % (name, failure.value))

def upload_zones(zones):
    ''' function to upload the grouped zones '''
    for name in zones:
        loader = load_zone(name)
        loader.addCallback(zone_loaded, name, zones[name])
        loader.addErrback(zone_error, name)

def group_zones(header, rows):
    ''' group zones together for more efficient import '''
    zones = {}
    for row in rows:
        record = { k:v for k,v in zip(header, row) }
        zone = record['Zone']
        if zone not in zones:
            zones[zone] = []
        zones[zone].append(record)
    return zones

def read_csv(filename):
    ''' read data from CSV file '''
    zones = {}
    with open(filename) as csvfile:
        rows = csv.reader(csvfile)
        header = next(rows)
        zones = group_zones(header, rows)
    return zones

def import_dns(filename):
    ''' function to import the DNS data '''
    zones = read_csv(filename)
    upload_zones(zones)
    reactor.callLater(REACTOR_TIMEOUT, reactor.stop)
    reactor.run()

def usage():
    print('Usage: python %s [csv-file]' % os.path.basename(sys.argv[0]))
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = sys.argv[0].replace('.py', '.csv')
    if not os.path.isfile(filename):
        usage()
    import_dns(filename)
