import os
import re
import sys

from pprint import pprint

USER='Mom'
DUPE = re.compile(r'\(\d+\)')

def rename_pdf (base):
    cerner = re.compile(r'^(?P<report>.+?)\s(?P<mo>\d{2})-(?P<dy>\d{2})-(?P<yr>\d{4})(\s\((?P<cnt>\d+)\))?')
    if DUPE.search(base):
        change = cerner.sub('\g<yr>\g<mo>\g<dy> - \g<report>\g<cnt> %s.pdf' % USER, base)
        og = cerner.sub('\g<report> \g<mo>-\g<dy>-\g<yr>.pdf', base)
        ng = cerner.sub('\g<yr>\g<mo>\g<dy> - \g<report> %s.pdf' % USER, base)
        cg = cerner.sub('\g<yr>\g<mo>\g<dy> - \g<report>0 %s.pdf' % USER, base)
        if os.path.exists(og): os.rename(og, cg)
        if os.path.exists(ng): os.rename(ng, cg)
    else:
        change = cerner.sub('\g<yr>\g<mo>\g<dy> - \g<report> %s.pdf' % USER, base)
    os.rename('%s.pdf' % base, change)

def rename_xml (base):
    cerner = re.compile(r'^(?P<report>.+?)-(?P<mo>\d{2})(?P<dy>\d{2})(?P<yr>\d{4})(-to-\d{2}\d{2}\d{4})?(\s\((?P<cnt>\d+)\))?')
    if DUPE.search(base):
        change = cerner.sub('\g<yr>\g<mo>\g<dy> - Care Summary\g<cnt> %s.xml' % USER, base)
    else:
        change = cerner.sub('\g<yr>\g<mo>\g<dy> - Care Summary %s.xml' % USER, base)
    os.rename('%s.xml' % base, change)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        USER = sys.argv[1]

    if len(sys.argv) > 2:
        srcdir = sys.argv[2]
    else:
        srcdir = os.getcwd()

    onlyfiles = [f for f in os.listdir(srcdir) if os.path.isfile(os.path.join(srcdir, f))]
    for f in onlyfiles:
        base_ext = os.path.splitext(f)
        if base_ext[1] == '.xml': rename_xml(base_ext[0])
        if base_ext[1] == '.pdf': rename_pdf(base_ext[0])

