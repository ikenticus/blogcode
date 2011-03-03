#!/usr/bin/env python
# Convert an SNMP Extend command into an OID
# Should provide the same result as:
#   snmpwalk -v# -cpublic host 'NET-SNMP-EXTEND-MIB::nsExtendObjects'
# Usage: $0 snmpextendname

import os
import sys

nsExtObjs = '.1.3.6.1.4.1.8072.1.3.2'
nsExtOids = {
    '2.1.2.12' : 'nsExtendCommand',
    '2.1.3.12' : 'nsExtendArgs',
    '2.1.4.12' : 'nsExtendInput',
    '2.1.5.12' : 'nsExtendCacheTime',
    '2.1.6.12' : 'nsExtendExecType',
    '2.1.7.12' : 'nsExtendRunType',
    '2.1.20.12': 'nsExtendStorage',
    '2.1.21.12': 'nsExtendStatus',
    '3.1.1.12' : 'nsExtendOutput1Line',
    '3.1.2.12' : 'nsExtendOutputFull',
    '3.1.3.12' : 'nsExtendOutNumLines',
    '3.1.4.12' : 'nsExtendResult',
    '4.1.2.12' : 'nsExtendOutLine',
}


def convert(cmd):
    oid = []
    for c in list(cmd):
        oid.append(str(ord(c)))
    oid = '.'.join(oid)
    for o in sorted(nsExtOids.keys()):
        print '%s.%s.%s\t%s."%s"' % (nsExtObjs, o, oid, nsExtOids[o], cmd)


if len(sys.argv) < 2:
    print 'Usage: %s SNMPExtendCommand' % os.path.basename(sys.argv[0])
    sys.exit(1)
else:
    convert(sys.argv[1])

