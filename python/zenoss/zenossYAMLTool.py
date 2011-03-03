#!/usr/bin/env python
#
# Author: ikenticus
# Created: April 2010
# Version: 11.03
#
# After discovering that deleting ZenPacks will remove all
# associated devices with no method of recovery except for
# pulling from a full ZenBackup, decided to develop an
# alternative means of export/import.
#
# The Linux Dynasty Zenoss_Template_Manager had the right
# idea, but in trying to manage it more effectively, I
# decided that I'd rather have YAML files rather than
# passing the amount of switches needed for templates.
#

import os
import re
import sys
sys.path.append("$ZENHOME/lib/python")
sys.path.append("$ZENHOME/lib/python2.4/site-packages")
sys.path.append("/usr/lib64/python2.4/site-packages")
sys.path.append(os.path.dirname(sys.argv[0]))

import types
import yaml

import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit
import Products.ZenModel.Device as model
dmd = ZenScriptBase(connect=True,noopts=True).dmd


def usage(code):
    acts = ""
    for line in open(sys.argv[0]):
        if 'if action == \'' in line:
            acts += "    %s\n" % line.split("'")[1]
    print """
Usage: %s -s

    -h                          help, this usage screen
    -p                          purge all empty organizers
    -l                          list all devices
    -i file.yaml                import devices/templates from yaml file
    -d /Server/Linux[/host]     export device(s) from specified device organizer as yaml
    -w /Server/Linux[/host]     export maintenance window(s) from specified event class as yaml
    -t /Server/Linux[/host]     export template(s) from specified device organizer as yaml
    -t /Server/Linux/template   export specific template from device organizer as yaml
    -o /Java                    export osprocess(es) from specified process organizer as yaml
    -r /Graph\ Reports          export report(s) from specified report organizer as yaml
    -r /Graph\ Reports/web      export specific report from report organizer as yaml
    -e /App/Zeus                export event mapping(s) from specified events organizer as yaml
    -x /Perf/Snmp               export transforms from specified event class as yaml
    -c smsalert                 export event commands(s) from specified command name as yaml
    -u johndoe[,janedoe]        export specified csv user(s) and related settings
    -a johndoe                  export alerting rule(s) from specified user/group

Currently supported import actions:
%s
Extract example(s) from export methods above
    """ % (os.path.basename(sys.argv[0]), acts) 
    sys.exit(code)


spaces = 4
def indent(level, index):
    global spaces
    if spaces < 2: spaces = 2   # make sure minimum spacing
    right = ''
    if index:
        level -= 1
        right = '-' + (' ' * (spaces - 1))
    insert = ' ' * (level * spaces)
    return insert + right

        
def matchDataSource(tpl,ds):
    datasrc = None
    for d in tpl.getRRDDataSources():
        if d.id == ds:
            datasrc = d
            break
    return datasrc


def matchOrganizerTemplate(org,tpl):
    template = None
    for t in org.getRRDTemplates():
        if t.id == tpl:
            template = t
            break
    return template


def test_device(name):
    dev = dmd.Devices.findDevice(name)    
    if not dev: return False
    else: 	return True


def test_user(user):
    for u in dmd.ZenUsers.getUsers():
	if str(user) == str(u):
            return u


def test_eventclass(evt):
    for e in dmd.Events.getInstances():
        if e.getEventClass() == evt:
            return e


def test_processclass(ops):
    for po in dmd.Processes.getOrganizerNames():
        if po == ops:
            return po


def test_reportclass(rpt):
    for ro in dmd.Reports.getOrganizerNames():
        if ro == rpt:
            return ro


def test_process(oc,ops):
    for o in oc.getSubOSProcessClassesSorted():
        if o.id == ops:
            return o


def test_report(rc,rpt):
    for r in rc.reports():
        if r.id == rpt:
            return r


def test_window(obj,win):
    for w in obj.getMaintenanceWindows():
        if w.id == win:
            return w


def export_alerts(actMatch):
    alerts = None
    for g in dmd.ZenUsers.getAllGroupSettings():
        if g.id == actMatch:
            #print "Group: %s" % g
            alerts = g.getActionRules()
            owner = 'group'
            break
    for u in dmd.ZenUsers.getUsers():
	if str(actMatch) == str(u):
            #print "User: %s" % u
            alerts = u.getActionRules()
            owner = 'user'
            break
    if not alerts:
        print "Found no owner(s) named: %s" % actMatch
        return
    for a in alerts:
        dict = export_alert(a, owner, actMatch)
        try: list.append(dict)
        except: list = [ dict ] 
    print yaml.dump(list, default_flow_style=False)


def export_alert(alert, type, owner):
    block = {'action': 'add_alert'}
    block['alertName'] = alert.id
    block['alertType'] = type
    block['alertOwner'] = owner
    for aa in alert._properties:
        attr = getattr(alert, aa['id'])
        if attr:
            if aa['id'] == 'action':
                  block['alertAction'] = attr
            else: block[aa['id']] = attr
    list = []
    for aw in alert.windows():
        dict = {'name': aw.id}
        for aa in aw._properties:
            if aa['id'] not in ['skip','started']:
                attr = getattr(aw, aa['id'])
                if attr: dict[aa['id']] = attr
        try: list.append(dict)
        except: list = [ dict ] 
    block['alertWindows'] = list
    return block


def export_users(usrMatch):
    for user in usrMatch.split(','):
        dict = export_user(user)
        try: list.append(dict)
        except: list = [ dict ] 
    print yaml.dump(list, default_flow_style=False)


def export_user(user):
    block = {'action': 'add_user'}
    uid = None
    for u in dmd.ZenUsers.getUsers():
	if str(user) == str(u):
            uid = u
            break
    block['userName'] = str(uid)
    block['userRoles'] = uid.getRoles()
    block['userRoles'].remove('Authenticated')
    block['userGroups'] =  uid.getUserGroupSettingsNames()
    us = dmd.ZenUsers.getUserSettings(str(uid))
    for ua in us._properties:
        attr = getattr(us, ua['id'])
        if attr: block[ua['id']] = attr
    return block


def export_reports(rptMatch):
    list = []
    ro = '/'.join(rptMatch.split('/')[:-1])
    if rptMatch in dmd.Reports.getOrganizerNames():
        ro = rptMatch
        rc = dmd.Reports.getOrganizer(ro)
        for r in rc.reports():
            if re.match('/Graph Reports', ro):
                dict = export_graphreport(r,ro)
            elif re.match('/Multi-Graph Reports', ro):
                dict = export_multireport(r,ro)
            else:
                print "Not a support report class: %s" % ro
                continue
            try: list.append(dict)
            except: list = [ dict ] 
    elif ro in dmd.Reports.getOrganizerNames():
        rc = dmd.Reports.getOrganizer(ro)
        for r in rc.reports():
            if r.id == rptMatch.split('/')[-1]:
                if re.match('/Graph Reports', ro):
                    list = export_graphreport(r,ro)
                elif re.match('/Multi-Graph Reports', ro):
                    list = export_multireport(r,ro)
                else:
                    print "Not a support report class: %s" % ro
                    return
        if not list:
            print 'No report named %s found for %s' % (rptMatch.split('/')[-1], ro)
            return
    else:
        print "No reports found for: %s" % rptMatch
        return
    print yaml.dump(list, default_flow_style=False)


def export_graphreport(rpt,org):
    block = {'action': 'add_graphreport'}
    block['reportName'] = rpt.id
    block['reportPath'] = org
    for ra in rpt._properties:
        if re.match('comments', ra['id']): continue
        block[ra['id']] = getattr(rpt, ra['id'])
    list = []
    for rel in rpt.getElements():
        dict = {'graphName': rel.id}
        for rea in rel._properties:
            if re.search('comments|summary', rea['id']): continue
            dict[rea['id']] = getattr(rel, rea['id'])
        try: list.append(dict)
        except: list = [ dict ]
    block['Graphs'] = list
    return block


def export_multireport(rpt,org):
    block = {'action': 'add_multireport'}
    block['reportName'] = rpt.id
    block['reportPath'] = org
    for ra in rpt._properties:
        if re.match('comments', ra['id']): continue
        block[ra['id']] = getattr(rpt, ra['id'])
    list = []
    for rc in rpt.getCollections():
        dict = {'collectionName': rc.id}
        list1 = []
        for ri in rc.getItems():
            dict1 = {'collectionItem': ri.id}
            for ra in ri._properties:
                dict1[ra['id']] = getattr(ri, ra['id'])
            try: list1.append(dict1)
            except: list1 = [ dict1 ]
        dict['CollectionItems'] = list1
        try: list.append(dict)
        except: list = [ dict ]
    block['Collections'] = list
    list = []
    list1 = []
    for gd in rpt.getGraphDefs():
        dict = {'gdName': gd.id}
        for gda in gd._properties:
            attr = getattr(gd,gda['id'])
            if attr: dict[gda['id']] = attr
        for gp in gd.getGraphPoints():
            dict1 = {'gpName': gp.id}
            for gpa in gp._properties:
                attr = getattr(gp,gpa['id'])
                if attr: dict1[gpa['id']] = attr
            if 'sequence' not in dict1.keys(): dict1['sequence'] = 0
            try: list1.append(dict1)
            except: list1 = [ dict1 ]
        dict['GraphPoints'] = list1
        try: list.append(dict)
        except: list = [ dict ]
    block['GraphDefs'] = list
    list = []
    for gg in rpt.getGraphGroups():
        dict = {'ggName': gg.id}
        for gga in gg._properties:
            attr = getattr(gg,gga['id'])
            if attr: dict[gga['id']] = attr
        if 'sequence' not in dict.keys(): dict['sequence'] = 0
        try: list.append(dict)
        except: list = [ dict ]
    block['GraphGroups'] = list
    return block


def export_eventcommands(cmdMatch):
    list = None
    for c in dmd.ZenEventManager.commands():
        if re.match(cmdMatch, c['id']):
            dict = export_eventcommand(c)
            try: list.append(dict)
            except: list = [ dict ] 
    if not list:
        print "+ ERROR exporting command(s) matching %s" % cmdMatch
        return
    print yaml.dump(list, default_flow_style=False)


def export_eventcommand(cmd):
    block = {'action': 'add_eventcommand'}
    block['commandName'] = cmd['id']
    for cp in cmd._properties:
        block[cp['id']] = getattr(cmd, cp['id'])
    return block


def export_eventmappings(evtMatch):
    for e in dmd.Events.getInstances():
        if e.getEventClass() == evtMatch:
            dict = export_eventmapping(e)
            try: list.append(dict)
            except: list = [ dict ] 
    print yaml.dump(list, default_flow_style=False)


def export_eventmapping(evt):
    block = {'action': 'add_eventmapping'}
    block['eventName'] = evt.id
    block['eventPath'] = evt.getEventClass() 
    for ea in evt._properties:
        attr = getattr(evt,ea['id'])
        if attr: block[ea['id']] = attr
    return block


def export_transforms(evtClass):
    block = {'action': 'add_transforms'}
    block['eventClass'] = evtClass
    block['eventTransforms'] = dmd.Events.getOrganizer(evtClass).transform
    print yaml.dump([block], default_flow_style=False)


def export_osprocesses(opsMatch):
    for oo in dmd.Processes.getOrganizerNames():
        if not re.match(opsMatch, oo): continue
        oc = dmd.Processes.getOrganizer(oo)
        for o in oc.getSubOSProcessClassesSorted():
            dict = export_osprocess(o, oo)
            try: list.append(dict)
            except: list = [ dict ] 
    print yaml.dump(list, default_flow_style=False)


def export_osprocess(ops, opsPath):
    block = {'action': 'add_osprocess'}
    block['psName'] = ops.id
    block['psPath'] = opsPath
    for op in ops._properties:
        attr = getattr(ops,op['id'])
	if op['id'] == 'name': continue
        if attr: block[op['id']] = attr
    return block


def export_windows(objMatch):
    obj = dmd.Devices.findDevice(objMatch.split('/')[-1])
    if obj:
        foundWindows = obj.getMaintenanceWindows()
    else:
        obj = dmd.Devices.getOrganizer(objMatch)
        foundWindows = obj.getMaintenanceWindows()
    for mw in foundWindows:
        dict = export_window(mw, objMatch)
        try: list.append(dict)
        except: list = [ dict ] 
    if not list:
        print "Unable to determine device/organizer based on input: %s" % objMatch
        return
    print yaml.dump(list, default_flow_style=False)



def export_window(win, winPath):
    block = {'action': 'add_window'}
    block['windowName'] = win.id
    block['windowPath'] = winPath
    block['enabled'] = win.enabled
    for wp in win._properties:
        attr = getattr(win,wp['id'])
	if wp['id'] == 'name': continue
        if attr: block[wp['id']] = attr
    return block


def export_devices(devMatch):
    dev = dmd.Devices.findDevice(devMatch.split('/')[-1])    
    if dev:
        list = export_device(dev)
    else:
        for d in dmd.Devices.deviceSearch():
            dev = dmd.Devices.findDevice(d.id)
            dpath = dev.getDeviceClassPath() 
            if dpath.startswith(devMatch):
                dict = export_device(dev)
                try: list.append(dict)
                except: list = [ dict ] 
    print yaml.dump(list, default_flow_style=False)


def export_device(dev, net=True):
    block = {'action': 'add_device'}
    block['deviceName'] = dev.id
    block['deviceHWTag'] = dev.getHWTag()
    block['devicePath'] = dev.getDeviceClassPath() 
    block['manageIp'] = dev.getManageIp()
    if dev.getLocationName():
        block['locationPath'] = dev.getLocationName()
    if dev.getSystemNames():
        block['systemPaths'] = dev.getSystemNames()
    if dev.getDeviceGroupNames():
        block['groupPaths'] = dev.getDeviceGroupNames()
    if net:
        block['devinterfaces'] = []
        for dc in dev.getDeviceComponents():
            for dca in dc._properties:
                if dca['id'] == 'interfaceName':
                    block['devinterfaces'].append(dc.id)
    return block


def export_templates(objMatch):
    singleTemplate = None
    try:
        obj = dmd.Devices.findDevice(objMatch.split('/')[-1])
        if obj:
            foundTemplates = obj.getRRDTemplates()
        else:
            obj = dmd.Devices.getOrganizer(objMatch)
            foundTemplates = obj.getRRDTemplates()
    except:
        singleTemplate = objMatch.split('/')[-1]
        try:
            obj = dmd.Devices.findDevice(objMatch.split('/')[-2])
            if obj:
                foundTemplates = obj.getRRDTemplates()
            else:
                obj = dmd.Devices.getOrganizer('/'.join(objMatch.split('/')[:-1]))
                foundTemplates = obj.getRRDTemplates()
        except:
            print "Unable to determine device/organizer based on input: %s" % objMatch
            return
    for tpl in foundTemplates:
        if singleTemplate:
            if tpl.id != singleTemplate: continue
            list = export_template(tpl)
        else:
            # only dump the 'bound' templates
            if not tpl.id in obj.zDeviceTemplates: continue
            dict = export_template(tpl)
            try: list.append(dict)
            except: list = [ dict ] 
    if not list:
        print "Unable to determine device/organizer based on input: %s" % objMatch
        return
    print yaml.dump(list, default_flow_style=False)


def export_template(tpl):
    # create the sourcetype map only once
    stmap = tpl.getDataSourceOptions()
    block = {'action': 'add_template'}
    block['templateName'] = tpl.id
    block['templatePath'] = re.sub(r'^.*dmd(.+)/'+tpl.id+'$', r'\1', tpl.getPrimaryUrlPath())
    block['templatePath'] = block['templatePath'].replace('/rrdTemplates', '')
    for ta in tpl._properties:
        attr = getattr(tpl,ta['id'])
        if attr: block[ta['id']] = attr
    list1 = []
    for ds in tpl.getRRDDataSources():
        dict1 = {'dsName': ds.id}
        dict1['enabled'] = False; # if True, getattr below will overwrite this
        for dsa in ds._properties:
            attr = getattr(ds,dsa['id'])
            if attr:
                dict1[dsa['id']] = attr
                # remap source type as full source option
                if dsa['id'] == 'sourcetype':
                    for st in stmap:
                        if st[0] == attr:
                            dict1[dsa['id']] = st[1]
                            continue
        list2 = []
        for dp in ds.getRRDDataPoints():
            dict2 = {'dpName': dp.id}
            for dpa in dp._properties:
                attr = getattr(dp,dpa['id'])
                if attr: dict2[dpa['id']] = attr
            try: list2.append(dict2)
            except: list2 = [ dict2 ]
        dict1['DataPoints'] = list2
        try: list1.append(dict1)
        except: list1 = [ dict1 ]
    block['DataSources'] = list1
    list1 = []
    for th in tpl.getGraphableThresholds():
        dict1 = {'thresholdName': th.id}
        for tha in th._properties:
            attr = getattr(th,tha['id'])
            dict1[tha['id']] = attr
        try: list1.append(dict1)
        except: list1 = [ dict1 ]
    block['Thresholds'] = list1
    list1 = []
    for gd in tpl.getGraphDefs():
        dict1 = {'gdName': gd.id}
        for gda in gd._properties:
            #print "    Setting %s.%s = %s" % (gd.id, gda, gda['id'])
            attr = getattr(gd,gda['id'])
            if attr: dict1[gda['id']] = attr
        list2 = []
        for gp in gd.getGraphPoints():
            dict2 = {'gpName': gp.id}
            for gpa in gp._properties:
                attr = getattr(gp,gpa['id'])
                if attr: dict2[gpa['id']] = attr
            if 'sequence' not in dict2.keys(): dict2['sequence'] = 0
            try: list2.append(dict2)
            except: list2 = [ dict2 ]
        dict1['GraphPoints'] = list2
        try: list1.append(dict1)
        except: list1 = [ dict1 ]
    block['GraphDefs'] = list1
    return block


def list_devices():
    for d in dmd.Devices.deviceSearch():
        dev = dmd.Devices.findDevice(d.id)
	item = '%s/%s' % (dev.getDeviceClassPath(), dev.id)
        try: list.append(item)
        except: list = [ item ] 
    print yaml.dump(sorted(list), default_flow_style=False)


def list_org(type):
    if type == "sys" or type == "Systems":
        return dmd.Systems.getOrganizerNames()
    elif type == "grp" or type == "Groups":
        return dmd.Groups.getOrganizerNames()
    elif type == "loc" or type == "Locations":
        return dmd.Locations.getOrganizerNames()
    elif type == "evt" or type == "Events":
        return dmd.Events.getOrganizerNames()
    else:
        return dmd.Devices.getOrganizerNames()


def delete_org(type,name):
    if type == "sys" or type == "Systems":
        dmd.Systems.manage_deleteOrganizer(name)
    elif type == "grp" or type == "Groups":
        dmd.Groups.manage_deleteOrganizer(name)
    elif type == "loc" or type == "Locations":
        dmd.Locations.manage_deleteOrganizer(name)
    elif type == "evt" or type == "Events":
        dmd.Events.manage_deleteOrganizer(name)
    else:
        print "Unknown organizer type: %s" % (type)


def purge_empty_orgs():
    pruned = False
    for type in [ 'Systems', 'Groups', 'Locations']:
        #print "\nListing orgs in %s" % (type)
        orgs = list_org(type)
        if not orgs:
            continue
        for org in orgs:
            # no need to remove top-level
            if org == '/':
                continue
            # query API using correct type
            if type == "Systems":
                sub = dmd.Systems.getOrganizer(org).getSubOrganizers()
                dev = dmd.Systems.getOrganizer(org).getDevices()
            elif type == "Groups":
                sub = dmd.Groups.getOrganizer(org).getSubOrganizers()
                dev = dmd.Groups.getOrganizer(org).getDevices()
            elif type == "Locations":
                sub = dmd.Locations.getOrganizer(org).getSubOrganizers()
                dev = dmd.Locations.getOrganizer(org).getDevices()
            # check if subs present
            if not sub and not dev:
                print " -%s organizer %s is empty, removing" % (type,org)
                delete_org(type,org)
                pruned = True
            #else:
            #    print "  %s organizer %s has children, leaving" % (type,org)
    return pruned


def import_yaml(file):
    f = open(file)
    yml = yaml.load(f)
    f.close()

    for block in yml:
        action = block['action']
        del block['action']
    
        if action == 'del_device':
            dname = block['deviceName']
            dev = dmd.Devices.findDevice(dname)
            print "+ DELETING device %s" % dname
            dev.deleteDevice()
            commit()
    
        elif action == 'ren_device':
            dname = block['deviceName']
            dev = dmd.Devices.findDevice(dname)
            print "+ RENAMING device %s" % dname
            if 'manageIp' in block:
                dev.setManageIp(block['manageIp'])
            dev.renameDevice(newId=block['deviceNewName'])
            commit()

        elif action == 'add_device':
            dname = block['deviceName']
            hwTag = None
            setIp = None
            if 'deviceHWTag' in block:
                hwTag = block['deviceHWTag']
                del block['deviceHWTag']
            if 'manageIp' in block:
                setIp = block['manageIp']
                del block['manageIp']
            dev = dmd.Devices.findDevice(dname)
            if not test_device(dname):
                print "+ ADDING device %s" % dname
                if setIp:
                    dev = model.manage_createDevice(dmd, dname,
                        devicePath=block['devicePath'],
                        discoverProto="none")
                    if dev:
                        del block['deviceName']
                        del block['devicePath']
                        dev.manage_editDevice(dmd, dname, **block)
                        dev.setManageIp(setIp)
                        commit()
                else:
                    dmd.DeviceLoader.loadDevice(**block)
                if hwTag: dev.setHWTag(hwTag)
                commit()
            else:
                print "+ MODIFYING %s" % dname
                del block['deviceName']
                dpath = block['devicePath'].replace('/Devices','',1)
                del block['devicePath']
                if dpath != dev.getDeviceClassPath():
                    dcExists = False
                    for o in list_org('devices'):
                        if o == dpath:
                            dcExists = True
                            break
                    if not dcExists:
                        print " - %s does not exist, creating" % dpath
                        dmd.Devices.getOrganizer('/').manage_addOrganizer(dpath)
                    dev.changeDeviceClass(dpath)
                #dev.manage_editDevice(dmd, dname, **block)
                if hwTag: dev.setHWTag(hwTag)
                if setIp: dev.setManageIp(setIp)
                commit()

        elif action == 'add_osprocess':
            opath = block['psPath']
            del block['psPath']
            if not test_processclass(opath):
                print "+ ADDING OS Process Class %s" % opath
                ops = dmd.Processes.getOrganizer('/')
                ops.manage_addOrganizer(opath)
                commit()
            ops = dmd.Processes.getOrganizer(opath)
            oname = block['psName']
            del block['psName']
            ps_exists = None
            for oc in ops.getSubOSProcessClassesSorted():
                if oc.id == oname:
                    ps_exists = oc
                    break
            if not ps_exists:
                print "+ ADDING OS Process %s" % oname
                op = ops.manage_addOSProcessClass(oname)
            for key in block.keys():
                if type(block[key]) is not types.ListType:
                    setattr(op,key,block[key])
            commit()

        elif action == 'del_user':
            uname = block['userName']
            print "+ DELETING user %s" % uname
            dmd.ZenUsers.manage_deleteUsers([uname])
            commit()

        elif action == 'add_user':
            uname = block['userName']
            if test_user(uname):
                print "+ USER %s already exists" % uname
            else:
                print "+ ADDING user %s" % uname
                dmd.ZenUsers.manage_addUser(uname, None, block['userRoles'], None, **block)
            if block['userGroups']:
                allgrps = [ g.id for g in dmd.ZenUsers.getAllGroupSettings() ]
                for g in block['userGroups']:
                    if g not in allgrps:
                        print " - Group (%s) does not exist, creating" % g
                        dmd.ZenUsers.manage_addGroup(g)
                        commit()
                print " - Adding user to: " + str(block['userGroups'])
                dmd.ZenUsers.manage_addUsersToGroups([uname], block['userGroups'])
            commit()
            if 'resetPassword' in block:
                if block['resetPassword']:
                    usr = dmd.ZenUsers.acl_users.getUser(uname)
                    # Not sure why this does NOT work
                    #dmd.ZenUsers.acl_users.getUser(uname).manage_resetPassword()

        elif action == 'add_multireport':
            rpath = block['reportPath']
            rc = ''
            for r in rpath.split('/'):
                if r:
                    rc += '/'
                    ro = dmd.Reports.getOrganizer(rc)
                    rc += r
                    if not test_reportclass(rc):
                        print "+ ADDING Report Class %s" % rc
                        ro.manage_addReportClass(r)
                        commit()
            ro = dmd.Reports.getOrganizer(rpath)
            rname = block['reportName']
            if not test_report(ro,rname):
                print "+ ADDING Report %s" % rname
                rpt = ro.manage_addMultiGraphReport(rname)
                commit()
            for r in ro.reports():
                if r.id == rname:
                    rpt = r
            for key in block.keys():
                if type(block[key]) is not types.ListType:
                    if key.startswith('report'): continue
                    setattr(rpt,key,block[key])
                    commit()
                else:
                    if key == 'Collections':
                        for e in block[key]:
                            cname = e['collectionName']
                            for rc in rpt.getCollections():
                                if rc.id == cname:
                                    print " - Deleting existing Collection %s" % cname
                                    rpt.manage_deleteCollections([cname])
                            print " - Adding Collection %s" % cname
                            rc = rpt.manage_addCollection(cname)
                            commit()
                            for ri in e['CollectionItems']:
                                devClass = systems = groups = locations = []
                                if ri['deviceId']:
                                    itemType = 'devcomp'
                                elif ri['deviceOrganizer'].startswith('/Devices'):
                                    itemType = 'deviceClass'
                                    devClass = [ri['deviceOrganizer']]
                                elif ri['deviceOrganizer'].startswith('/Systems'):
                                    itemType = 'system'
                                    systems = [ri['deviceOrganizer']]
                                elif ri['deviceOrganizer'].startswith('/Groups'):
                                    itemType = 'group'
                                    groups = [ri['deviceOrganizer']]
                                elif ri['deviceOrganizer'].startswith('/Locations'):
                                    itemType = 'location'
                                    locations = [ri['deviceOrganizer']]
                                else:
                                    continue
                                print " - Adding Collection Item Type %s" % itemType
                                rc.manage_addCollectionItem(itemType, [ri['deviceId']], [ri['compPath']],
                                    devClass, systems, groups, locations, ri['recurse'])
                                commit()
                    elif key == 'GraphDefs':
                        for gd in block[key]:
                            gdo = rpt.manage_addGraphDefinition(gd['gdName'])
                            gdo.manage_deleteGraphPoints(gdo.getGraphPointsNames())
                            for gda in gd.keys():
                                if gda != 'GraphPoints':
                                    setattr(gdo,gda,gd[gda])
                            gpl = []
                            gpdp = []
                            gpth = []
                            for gp in gd['GraphPoints']:
                                gpl.append(gp['gpName'])
                                if 'threshId' in gp.keys():
                                    gpth.append(gp['gpName'])
                                else:
                                    gpdp.append(gp['gpName'])
                            if len(gpth):
                                print " - Adding Threshold Graph Point %s" % gp['gpName']
                                gdo.manage_addThresholdGraphPoints(gpth)
                            if len(gpdp):
                                print " - Adding DataPoint Graph Point %s" % gp['gpName']
                                gdo.manage_addDataPointGraphPoints(gpdp)
                            for gp in gd['GraphPoints']:
                                for gpo in gdo.getGraphPoints():
                                    if gpo.id == gp['gpName']:
                                        for gpa in gp.keys():
                                            if gpa != 'gpName':
                                                setattr(gpo,gpa,gp[gpa])
                    elif key == 'GraphGroups':
                        for gg in block[key]:
                            print " - Adding Graph Group %s" % gg['ggName']
                            grp = rpt.manage_addGraphGroup(gg['ggName'],
                                gg['collectionId'], gg['graphDefId'])
                            for gk in gg:
                                if type(gg[gk]) is not types.StringType:
                                    setattr(grp, gk, gg[gk])

        elif action == 'add_graphreport':
            rpath = block['reportPath']
            rc = ''
            for r in rpath.split('/'):
                if r:
                    rc += '/'
                    ro = dmd.Reports.getOrganizer(rc)
                    rc += r
                    if not test_reportclass(rc):
                        print "+ ADDING Report Class %s" % rc
                        ro.manage_addReportClass(r)
                        commit()
            ro = dmd.Reports.getOrganizer(rpath)
            rname = block['reportName']
            if not test_report(ro,rname):
                print "+ ADDING Report %s" % rname
                rpt = ro.manage_addGraphReport(rname)
                commit()
            for r in ro.reports():
                if r.id == rname:
                    rpt = r
            for key in block.keys():
                if type(block[key]) is not types.ListType:
                    if key.startswith('report'): continue
                    setattr(rpt,key,block[key])
                    commit()
                else:
                    for e in block[key]:
                        gname = e['graphName']
                        for rel in rpt.getElements():
                            if rel.id == gname:
                                print " - Deleting existing Graph %s" % gname
                                rpt.manage_deleteGraphReportElements([gname])
                        print " - Adding Graph %s" % gname
                        rel = rpt.manage_addGraphElement(e['deviceId'],
                            [e['componentPath']], [e['graphId']])
                        commit()

        elif action == 'add_alert':
            alert = None
            aname = block['alertName']
            atype = block['alertType']
            aowner = block['alertOwner']
            if re.search(',', aowner):
                owners = aowner.split(',')
            else:
                owners = [ aowner ]
            for owner in owners:
                if atype == 'group':
                    for g in dmd.ZenUsers.getAllGroupSettings():
                        if g.id == owner:
                            owner = g
                            break
                elif atype == 'user':
                    for u in dmd.ZenUsers.getUsers():
                        if str(u) == owner:
                            owner = u
                            break
                else:
                    print "Invalid owner: %s" % owner
                    continue
                ar = None
                for oa in owner.getActionRules():
                    if oa.id == aname:
                        ar = oa.id
                        break
                if ar:
                    print "Owner (%s) already has alert: %s, modifying" % (owner,aname)
                else:
                    print "+ ADDING (%s) alert to %s" % (aname, owner)
                    owner.manage_addActionRule(aname)
                for ar in dmd.ZenUsers.getAllActionRules():
                    if ar.id == aname:
                        alert = ar
                        break
                if not alert:
                    print " - Unknown failure adding alert: %s" % aname
                    return
                block['action'] = block['alertAction']
                for key in block.keys():
                    if key.startswith('alert'): continue
                    setattr(alert,key,block[key])
                for w in block['alertWindows']:
                    ar.manage_addActionRuleWindow(w['name'])
                    commit()
                    win = None
                    for aw in ar.windows():
                        if aw.id == w['name']:
                            win = aw
                    for wa in w:
                        setattr(win, wa, w[wa])
                commit()

        elif action == 'del_eventmapping':
            ename = block['eventName']
            epath = block['eventPath']
            evt = dmd.Events.getOrganizer(epath)
            if not evt:
                print " - Event Class not found: %s" % epath
            else:
                inst_exists = None
                for ei in evt.getInstances():
                    if ei.id == ename:
                        inst_exists = ei
                        break
                if not inst_exists:
                    print " - Event Mapping not found: %s" % epath
                else:
                    print "+ DELETING Event Mapping %s" % ename
                    evt.removeInstances([ename])
                    if not len(evt.getInstances()):
                        print "+ DELETING Empty Event Class %s" % epath
                        delete_org('evt', epath)
            commit()

        elif action == 'add_eventcommand':
            cname = block['commandName']
            del block['commandName']
            print "+ ADDING Event Command: %s" % cname
            dmd.ZenEventManager.manage_addCommand(cname)
            cmd = None
            for c in dmd.ZenEventManager.commands():
                if c['id'] == cname:
                    cmd = c
            if cmd:
                for c in block.keys():
                    setattr(cmd, c, block[c])
                commit()

        elif action == 'add_eventmapping':
            epath = block['eventPath']
            if not test_eventclass(epath):
                print "+ ADDING Event Class %s" % epath
                evt = dmd.Events.getOrganizer('/')
		evt.manage_addOrganizer(epath)
                commit()
            evt = dmd.Events.getOrganizer(epath)
            ename = block['eventName']
            inst_exists = None
            for ei in evt.getInstances():
                if ei.id == ename:
                    inst_exists = ei
                    break
            if not inst_exists:
                print "+ ADDING Event Mapping (Instance) %s" % ename
                ei = evt.createInstance(ename)
		#print ei._properties
		for p in ei._properties:
                    if p['id'] is not 'sequence':
                        if not p['id'] in block: block[p['id']] = ''
                # setattr does not work correctly, nor does **block
                ei.manage_editEventClassInst(
                    block["eventName"],
                    block["eventClassKey"],
                    block["rule"],
                    block["regex"],
                    block["example"],
                    block["transform"],
                    block["explanation"],
                    block["resolution"])
                commit()

        elif action == 'del_transforms':
            evt = dmd.Events.getOrganizer(block['eventClass'])
            evt.manage_editEventClassTransform(transform = '')
            commit()

        elif action == 'add_transforms':
            eclass = block['eventClass']
            if not test_eventclass(eclass):
                print "+ ADDING Event Class %s" % eclass
                evt = dmd.Events.getOrganizer('/')
		evt.manage_addOrganizer(eclass)
                commit()
            evt = dmd.Events.getOrganizer(eclass)
            evt.manage_editEventClassTransform(transform = block['eventTransforms'])
            commit()

        elif action == 'del_window':
            wname = block['windowName']
            print "+ DELETING window %s" % wname
            obj = dmd.Devices.findDevice(block['windowPath'].split('/')[-1])
            if obj:
                obj.manage_deleteMaintenanceWindow([wname])
            else:
                obj = dmd.Devices.getOrganizer(block['windowPath'])
                if obj:
                    obj.manage_deleteMaintenanceWindow([wname])
            commit()
    
        elif action == 'add_window':
            win = None
            obj = dmd.Devices.findDevice(block['windowPath'].split('/')[-1])
            if obj:
                win = test_window(obj,block['windowName'])
                if win:
                    print "+ EDITING existing window %s for %s" % (block['windowName'], block['windowPath'])
                else:
                    print "+ ADDING window %s for %s" % (block['windowName'], block['windowPath'])
                    obj.manage_addMaintenanceWindow(block['windowName'])
            else:
                obj = dmd.Devices.getOrganizer(block['windowPath'])
                if obj:
                    win = test_window(obj,block['windowName'])
                    if win:
                        print "+ EDITING existing window %s for %s" % (block['windowName'], block['windowPath'])
                    else:
                        print "+ ADDING window %s for %s" % (block['windowName'], block['windowPath'])
                        obj.manage_addMaintenanceWindow(block['windowName'])
            win = test_window(obj,block['windowName'])
            if not win:
                print "+ ERROR adding window %s" % block['windowName']
                break
            else:
                for w in block.keys():
                    setattr(win, w, block[w])
                commit()

        elif action == 'del_template':
            tname = block['templateName']
            print "+ DELETING template %s" % tname
            obj = dmd.Devices.findDevice(block['templatePath'].split('/')[-1])
            if obj:
                obj.manage_deleteRRDTemplates([tname])
            else:
                obj = dmd.Devices.getOrganizer(block['templatePath'])
                if obj:
                    obj.manage_deleteRRDTemplates([tname])
            bindings = obj.zDeviceTemplates
            if tname in bindings:
                bindings.remove(tname)
                obj.bindTemplates(bindings)
                commit()
    
        elif action == 'add_template':
            tpl = None
            obj = dmd.Devices.findDevice(block['templatePath'].split('/')[-1])
            if obj:
                tpl = obj.getRRDTemplateByName(block['templateName'])
                if tpl:
                    print "+ EDITING existing template %s for %s" % (block['templateName'], block['templatePath'])
                else:
                    print "+ ADDING template %s for %s" % (block['templateName'], block['templatePath'])
                    obj.addLocalTemplate(block['templateName'])
                    tpl = obj.getRRDTemplateByName(block['templateName'])
            else:
                obj = dmd.Devices.getOrganizer(block['templatePath'])
                if obj:
                    tpl = matchOrganizerTemplate(obj,block['templateName'])
                    if tpl:
                        print "+ EDITING existing template %s for %s" % (block['templateName'], block['templatePath'])
                    else:
                        print "+ ADDING template %s for %s" % (block['templateName'], block['templatePath'])
                        obj.manage_addRRDTemplate(block['templateName'])
                        tpl = matchOrganizerTemplate(obj,block['templateName'])
            if not tpl:
                print "+ ERROR adding template %s" % block['templateName']
                break
            else:
                for key in block.keys():
                    if type(block[key]) is not types.ListType:
                        if key.startswith('template'): continue
                        #print "  Setting %s.%s to %s" % (tpl, key, block[key])
                        setattr(tpl,key,block[key])
                    else:
                        print " - Adding %s" % key
                        if key == 'DataSources':
                            for ds in block[key]:
                                try: dsOption = ds['sourcetype']
                                except: dsOption = 'BasicDataSource.COMMAND'
                                # sourcetype must be reset to short name to import properties below
                                ds['sourcetype'] = dsOption.split('.')[1]
                                dso = tpl.manage_addRRDDataSource(ds['dsName'], dsOption)
                                for dsa in ds.keys():
                                    if dsa != 'DataPoints':
                                        setattr(dso,dsa,ds[dsa])
                                    else:
                                        for dp in ds[dsa]:
                                            dpo = dso.manage_addRRDDataPoint(dp['dpName'])
                                            for dpa in dp.keys():
                                                if dpa != 'dpName':
                                                    setattr(dpo,dpa,dp[dpa])
                        elif key == 'Thresholds':
                            for th in block[key]:
                                try: thClass = th['type']
                                except: thClass = 'MinMaxThreshold'
                                tho = tpl.manage_addRRDThreshold(th['thresholdName'], thClass)
                                for tha in th.keys():
                                    if tha != 'thresholdName':
                                        setattr(tho,tha,th[tha])
                        elif key == 'GraphDefs':
                            for gd in block[key]:
                                #print "    Graph: %s" % gd['gdName']
                                gdo = tpl.manage_addGraphDefinition(gd['gdName'])
                                # need to delete existing GraphPoints to avoid replication
                                gdo.manage_deleteGraphPoints(gdo.getGraphPointsNames())
                                for gda in gd.keys():
                                    if gda != 'GraphPoints':
                                        setattr(gdo,gda,gd[gda])
                                gpl = []
                                gpdp = []
                                gpth = []
                                for gp in gd['GraphPoints']:
                                    #print "        %s" % gp['gpName']
                                    gpl.append(gp['gpName'])
                                    if 'threshId' in gp.keys():
                                        gpth.append(gp['gpName'])
                                    else:
                                        gpdp.append(gp['gpName'])
                                if len(gpth):
                                    gdo.manage_addThresholdGraphPoints(gpth)
                                if len(gpdp):
                                    gdo.manage_addDataPointGraphPoints(gpdp)
                                for gp in gd['GraphPoints']:
                                    for gpo in gdo.getGraphPoints():
                                        if gpo.id == gp['gpName']:
                                            for gpa in gp.keys():
                                                if gpa != 'gpName':
                                                    #print "    Setting %s.%s to %s" % (gp['gpName'], gpa, gp[gpa])
                                                    setattr(gpo,gpa,gp[gpa])
            bindings = obj.zDeviceTemplates
            bindings.append(tpl.id)
            obj.bindTemplates(bindings)
            commit()


def main (args):
    # parse/process command line options/arguments
    import getopt
    try:
        opts, args = getopt.getopt(args, "Aa:d:c:e:hi:lo:pr:t:u:w:x:",
            [ '--help', '--device', '--event', '--template', '--osprocess', '--import',
              '--user', '--alert', '--report', '--command', '--purge', '--list',
              '--transform', '--window' ])
    except getopt.error:
        usage(3)

    if not opts:
        usage(3)

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage(3)
        if opt in ('-i', '--import'):
            import_yaml(val)
        if opt in ('-a', '--alert'):
            export_alerts(val)
        if opt in ('-c', '--command'):
            export_eventcommands(val)
        if opt in ('-d', '--device'):
            export_devices(val)
        if opt in ('-e', '--event'):
            export_eventmappings(val)
        if opt in ('-o', '--osprocess'):
            export_osprocesses(val)
        if opt in ('-r', '--report'):
            export_reports(val)
        if opt in ('-t', '--template'):
            export_templates(val)
        if opt in ('-u', '--user'):
            export_users(val)
        if opt in ('-x', '--transform'):
            export_transforms(val)
        if opt in ('-w', '--window'):
            export_windows(val)
        if opt in ('-p', '--purge'):
            purge_empty_orgs()
            sys.exit(0)
        if opt in ('-l', '--list'):
            list_devices()
            sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])

