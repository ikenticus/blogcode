#!/usr/bin/env python
#
# Author: ikenticus
# Created: May 2011
# Suummary: Automatically generate Multi-Report Screens from DeviceClasses
#

import os
import re
import sys
import ConfigParser
import zenossYAMLTool as z
from pprint import pprint

# retrieve conf file using current script name
cfname = sys.argv[0].replace('.py', '.cf')
conf = ConfigParser.ConfigParser()
conf.read(cfname)

class NextGraph(Exception): pass

def build_group(id, combine=True, title='', seq=0):
    return {
        'collectionId': id,
        'combineDevices': combine,
        'ggName': title,
        'graphDefId': title,
        'sequence': seq
        }

def build_collitem(name='Item', id='', comp='', org='', seq=0):
    return {
        'collectionItem': name,
        'compPath': comp,
        'deviceId': id,
        'deviceOrganizer': '/Devices' + org,
        'recurse': False,
        'sequence': seq
        }

def build_processes(dclass, seq):
    graphs = []
    groups = []
    pgroups = []
    colls = []
    for gpName in conf.get('processes', 'include').split(','):
        seq = seq + 1
        newgraph, newgroup = convert_graphs(gpName, seq, dclass, '/Server/OSProcess')
        graphs.append(newgraph)
        pgroups.append(newgroup)
    for g in graphs:
        g['gdName'] = g['gdName'].replace('Used', 'Process')
    ps = {}
    cnt = -1
    for d in sorted(z.export_devices(dclass, ps=True)):
        cnt = cnt + 1
        for p in sorted(d['processes']):
            if p not in ps.keys():
                ps[p] = []
            ps[p].append(build_collitem(comp='os/processes/%s' % p,
                id=d['deviceName'], seq=cnt))
    plist = z.list_processhash()
    for p in ps:
        pname = p.split('-')[0].split('_')[-1]
        if pname.startswith('java'):
            for ph in plist:
                if ph['md5'] in pname:
                    pname = '%s %s' % (pname.split(' ')[0], re.sub('=(\w+).*$', r' \1', ph['parameters'].split(' ')[0]))
        colls.append({ 'collectionName': '%s %s process' % (dclass.split('/')[-1], pname),
          'CollectionItems': ps[p] })
        for pg in pgroups:
           pgroup = {}
           for k in pg.keys():
               if k == 'collectionId':
                   pgroup[k] = '%s %s process' % (dclass.split('/')[-1], pname)
               elif k == 'ggName':
                   pgroup[k] = '%s %s' % (pg[k].replace('Used', 'Process'), pname)
               elif k == 'graphDefId':
                   pgroup[k] = pg[k].replace('Used', 'Process')
               elif k == 'sequence':
                   pgroup[k] = seq
               else:
                   pgroup[k] = pg[k]
               seq = seq + 1
           groups.append(pgroup)
    return colls, groups, graphs, seq

def build_filesystems(dclass, seq):
    graphs = []
    groups = []
    colls = []
    seq = seq + 1
    newgraph, newgroup = convert_graphs('usedBlocks', seq, dclass, '/Server/FileSystem')
    graphs.append(newgraph)
    fs = {}
    cnt = -1
    excludes = conf.get('filesystems', 'exclude').split(',')
    for d in sorted(z.export_devices(dclass, disk=True)):
        for f in sorted(d['filesystems']):
            skip = False
            for e in excludes:
                if f.startswith(e):
                    skip = True
                    break
            if not skip:
                if f not in fs.keys():
                    fs[f] = []
                cnt = cnt + 1
                fs[f].append(build_collitem(comp='os/filesystems/%s' % f,
                    id=d['deviceName'], seq=cnt))
    for f in fs:
        fname = re.sub('^-$', 'root', f)
        colls.append({ 'collectionName': '%s %s filesystem' % (dclass.split('/')[-1], fname),
          'CollectionItems': fs[f] })
        fgroup = {}
        for k in newgroup.keys():
            if k == 'collectionId':
                fgroup[k] = '%s %s filesystem' % (dclass.split('/')[-1], fname)
            elif k == 'ggName':
                fgroup[k] = 'Disk %s %s' % (newgroup[k], fname)
            else:
                fgroup[k] = newgroup[k]
        groups.append(fgroup)
    return colls, groups, graphs, seq

def build_interfaces(dclass, seq):
    graphs = []
    groups = []
    intf = conf.get('interfaces', 'collection').split('=')
    for gpName in conf.get('interfaces', 'include').split(','):
        seq = seq + 1
        newgraph, newgroup = convert_graphs(gpName, seq, dclass, '/Server/ethernetCsmacd')
        graphs.append(newgraph)
        groups.append(newgroup)
    for g in groups:
        g['collectionId'] = '%s %s interface' % (dclass.split('/')[-1], intf[0])
    cnt = -1
    colls = { 'collectionName': '%s %s interface' % (dclass.split('/')[-1], intf[0]),
              'CollectionItems': [] }
    for d in sorted(z.export_devices(dclass, net=True)):
        for i in intf[1].split('|'):
            if i in d['interfaces']:
                cnt = cnt + 1
                colls['CollectionItems'].append(build_collitem(comp='os/interfaces/%s' % i,
                    id=d['deviceName'], seq=cnt))
                break
    return [colls], groups, graphs, seq

def build_common(dclass, seq):
    graphs = []
    groups = []
    for gpName in conf.get('common', 'include').split(','):
        seq = seq + 1
        newgraph, newgroup = convert_graphs(gpName, seq, dclass, dclass)
        graphs.append(newgraph)
        groups.append(newgroup)
    colls = { 'collectionName': dclass.split('/')[-1],
        'CollectionItems': [ build_collitem(org=dclass) ] }
    return [colls], groups, graphs, seq

def convert_graphs(gpName, seq, dclass, tpl):
    for t in z.export_templates(tpl):
        try:
            for g in t['GraphDefs']:
                for p in g['GraphPoints']:
                    if p['gpName'] == gpName:
                        g['gdName'] = '%s (%s)' % (g['gdName'], p['legend'])
                        newgraph = g
                        p['legend'] = '${dev/id | here/name | here/id} ${graphPoint/id}'
                        p['lineType'] = 'LINE'
                        p['sequence'] = seq
                        newgraph['GraphPoints'] = [p]
                        newgraph['GraphPoints'] = [p]

                        newgroup = build_group(dclass.split('/')[-1],
                            title=g['gdName'], seq=seq)
                        raise NextGraph
        except NextGraph:
            break
    return newgraph, newgroup

def build_report(dclass):
    seq = -1
    colls, groups, graphs, seq = build_common(dclass, seq)
    report = {
        'action': 'add_multireport',
        'numColumns': 2, 'title': '',
        'reportName': dclass.split('/')[-1],
        'reportPath': '/Multi-Graph Reports/Screens',
        'GraphGroups': groups,
        'Collections': colls,
        'GraphDefs': graphs, }

    colls, groups, graphs, seq = build_interfaces(dclass, seq)
    report['Collections'].extend(colls)
    report['GraphGroups'].extend(groups)
    report['GraphDefs'].extend(graphs)

    colls, groups, graphs, seq = build_processes(dclass, seq)
    report['Collections'].extend(colls)
    report['GraphGroups'].extend(groups)
    report['GraphDefs'].extend(graphs)

    colls, groups, graphs, seq = build_filesystems(dclass, seq)
    report['Collections'].extend(colls)
    report['GraphGroups'].extend(groups)
    report['GraphDefs'].extend(graphs)

    #pprint(report)
    z.import_yaml([report])

def main (args):
    single = None
    if len(args) > 0:
        single = args[0]

    for dclass in sorted(list(set(['/'.join(dc.split('/')[0:-1])
        for dc in z.list_devices() if dc.startswith('/Server')]))):
        if not single or dclass.split('/')[3] == single:
            build_report(dclass)

if __name__ == "__main__":
    main(sys.argv[1:])
