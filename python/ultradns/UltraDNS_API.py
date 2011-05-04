"""
UltraDNS API Script

Author:     ikenticus
Created:    2011-04-29
Updated:    2011-05-03
Summary:    Interactive modular class for querying UltraDNS XML-RPC
"""

import os
import re
import sys
import socket
import urllib
import ConfigParser

from OpenSSL import SSL
from pyPdf import PdfFileReader
from xml.etree import ElementTree as ET

# global settings
pdfurl = 'https://www.ultradns.net/api/NUS_API_XML.pdf'


class UltraDNS:
    def __init__(self, cfname, pdfname, debug=False):
        self.root = None
        self.cfname = cfname
        self.config = ConfigParser.ConfigParser()
        self.config.read(cfname)
        self.workdir = '/tmp/'

        cf = {'url': {'server':'api.ultradns.net', 'port':8755},
            'auth': {'sponsor':'ultradnsweb', 'username':'', 'password':''}}
        if not self.config._sections:
            self.parse_pdf(pdfname)
            print 'Missing configuration file'
            for section in cf.keys():
                self.config.add_section(section)
                for option in cf[section].keys():
                    self.request_option(section, option, cf[section][option])
            self.save_config()
        self.methods = sorted([ m for m in self.config._sections
            if m.startswith('UDNS_') ])

    def request_option(self, section, option, old=''):
        if option in self.config.options(section):
            old = self.config.get(section, option)
        try:
            ans = ''
            while ans =='':
                ans = raw_input('  Setting %s[%s]: ' % (option, old))
                if not ans:
                    ans = old
        except KeyboardInterrupt, e:
            print '\nConfiguration aborted by user'
            sys.exit(1)
        self.config.set(section, option, ans)

    def parse_pdf(self, pdfname):
        if not os.path.exists(pdfname):
            print 'Missing API documentation, downloading from: %s' % pdfurl
            urllib.urlretrieve(pdfurl, pdfname)
        print 'Compiling API methods...'
        apidoc = PdfFileReader(file(pdfname, 'rb'))
        for p in range(0,apidoc.getNumPages()):
            doc = apidoc.getPage(p).extractText()
            mCall = re.search(r'<methodCall>.+</methodCall>', doc)
            mResp = re.search(r'<methodResponse>.+</methodResponse>', doc)
            section = None
            if mCall:
                xml = mCall.group()
                method = re.search(r'<methodName>(UDNS_\w+)</methodName>', xml)
                if not method:
                    continue
                section = method.group(1)
                if section not in self.config._sections:
                    self.config.add_section(section)
                patt = re.compile(r'<value><([^\s]+)>([^\s]+)</([^\s]+)></value>')
                match = re.findall(patt, xml)
                order = []
                for m in match:
                    key = '%s+%s' % m[0:2]
                    self.config.set(section, key, m[2])
                    order.append(key)
                if order:
                    self.config.set(section, 'order', ','.join(order))
            if section and re.search(r'<fault>', doc):
                    self.config.set(section, 'fault', True)
            if section and mResp:
                xml = mResp.group()
                record = re.search(r'<array>\s*<data>\s*<value>\s*<([_\w]+)>', xml)
                if record:
                    self.config.set(section, 'array', record.group(1))

    def save_config(self):
        file = open(self.cfname, 'w')
        self.config.write(file)
        file.close()

    def check_xml(self, method_name, params=None, cached=None):
        cache = self.workdir + method_name
        if 'Get' in method_name and os.path.exists(self.workdir + method_name):
            print 'Previously downloaded XML found for %s' % method_name
            if cached:
                ans = cached
            else:
                try:
                    ans = raw_input('Would you like to use cached copy? [Y/n]: ')
                except KeyboardInterrupt, e:
                    print '\n%s aborted by user' % self.plug
                    sys.exit(1)
            if ans.lower() != 'n':
                # reading XML from cached file
                print 'Loading Cached XML Response'
                tree = ET.ElementTree()
                tree.parse(cache)
                self.root = tree.getroot()
                return
        # reading XML directly from site
        print 'Submitting XML Request...'
        xml = '<methodCall><methodName>%s</methodName>' % method_name
        xml += '<params>%s</params></methodCall>' \
            % self.query_param(method_name, params)
        self.root = ET.XML(self.send_xml(method_name, xml))

    def send_xml(self, method_name, method_xml):
        xml_head = '<?xml version="1.0"?><transaction>'
        xml_foot = '<methodCall><methodName>UDNS_Disconnect</methodName>'
        xml_foot += '</methodCall></transaction>'

        xml_login = '<methodCall><methodName>UDNS_OpenConnection</methodName>'
        xml_login += '<params>'
        for c in ['sponsor', 'username', 'password']:
            xml_login += '<param><value><string>%s</string></value></param>'\
                % self.config.get('auth', c)
        xml_login += '<param><value><float>2.0</float></value></param>'
        xml_login += '</params></methodCall>'

        xml = xml_head + xml_login + method_xml + xml_foot
        conn = SSL.Context(SSL.TLSv1_METHOD)
        sock = SSL.Connection(conn,
            socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sock.connect((self.config.get('url', 'server'),
            int(self.config.get('url', 'port'))))
        sock.send(xml)
        ans = ''
        while 1:
            try:
                ans += sock.recv(1024)
            except SSL.ZeroReturnError:
                print 'XML Data Retrieval Completed'
                break
        if 'Get' in method_name:
            file = open(self.workdir + method_name, 'w')
            print >>file, ans
            file.close()
        sock.shutdown()
        sock.close()
        #print ans
        return ans

    def query_param(self, name, params=None):
        """
            parameters should be using the following syntax:
                { 'tagname+setting.': default_setting }
            such that the xml generated will map directly as:
                '<tagname>%s.</tagname>' % setting
            the trailing period only present in key if needed

            if override params are provided, the format should be:
                { 'setting': override_setting }
        """
        xml = ''
        if not params:
            print '%s requires the following settings:' % name
        for q in self.config.get(name, 'order').split(','):
            tag, setting = q.split('+')
            dot = ''
            if setting.rstrip('.') != setting:
                setting = setting.rstrip('.')
                dot = '.'
            old = self.config.get(name, q)
            ans = ''
            while ans == '':
                if params:
                    if setting in params.keys():
                        ans = params[setting]
                    else:
                        ans = old
                else:
                    try:
                        ans = raw_input('  Setting %s[%s]: ' % (setting, old))
                    except KeyboardInterrupt, e:
                        print '\n%s aborted by user' % self.plug
                        sys.exit(1)
                if not ans:
                    ans = old
            xml += '<param><value><%s>%s%s</%s></value></param>' \
                % (tag, ans, dot, tag)
            self.config.set(name, q, ans)
        # save current settings for next time
        self.save_config()
        return xml

    def loop_child(self, obj, target):
        children = None
        for o in obj:
            if o.tag != target:
                children = self.loop_child(o, target)
            else:
                return o.getchildren()
        return children

    def parse_value(self, obj, name):
        dict = {}
        for member in self.loop_child(obj, name):
             for x in member.getchildren():
                 if x.tag == 'name':
                     #print '\tKey: %s' % x.text
                     key = x.text
                 if x.tag == 'value':
                     #print '\tValue: %s' % x.getchildren()[0].text
                     dict[key] = x.getchildren()[0].text
        return dict

    def parse_xml(self, name, match=None):
        if not self.root:
            print 'No XML to parse'
            return
        if 'array' in self.config.options(name):
            results = []
            for record in self.loop_child(self.root[1], 'array')[0]:
                results.append(self.parse_value(record,
                    self.config.get(name, 'array')))
            if match:
                print 'Extracted %d Records' % len(results)
                matches = []
                m = match.split(':')
                if m[1] == 'None':
                    return results
                for r in results:
                    if m[0] in r and m[1] in r[m[0]]:
                        matches.append(r)
                if matches:
                    print matches
                else:
                    print 'No matches found'
            else:
                print results
        elif 'fault' in self.config.options(name):
            try:
                print self.parse_value(self.root.getchildren()[1], 'struct')
            except:
                print self.loop_child(self.root.getchildren()[3], 'param')[0].text
        else:
            print 'Unable to parse, iterating the results'
            for p in self.root.getiterator():
                try:
                    print '%s: %s' % (p.tag, p.text)
                except TypeError:
                    pass

    def choose_method(self, method=None, match=None, params=None, cached=None):
        default = ''
        if not method:
            print 'Currently available methods:'
            for m in self.methods:
                print '  %3d) %-30s' % (self.methods.index(m), m)
                if 'getcname' in m.lower():
                    default = self.methods.index(m)
            ans = ''
            while ans =='':
                try:
                    ans = raw_input('Which method do you want to execute [%s]: ' \
                        % str(default))
                except KeyboardInterrupt, e:
                    print '\n%s aborted by user' % self.plug
                    sys.exit(1)
                if not ans:
                    ans = default
            m = self.methods[int(ans)]
        else:
            m = method
        self.check_xml(m, params=params, cached=cached)
        self.parse_xml(m, match=match)


if __name__ == "__main__":
    # retrieve conf file using current script name
    cfname = sys.argv[0].replace('.py', '.cf')
    cfpath = os.path.dirname(sys.argv[0])
    if not cfpath:
        cfpath = os.getcwd()
    u = UltraDNS(cfname, cfpath+'/'+pdfurl.split('/')[-1])

    # interactive mode
    #u.choose_method()

    # automated answers
    #u.choose_method(method='UDNS_GetCNAMERecordsOfZone', cached='n',
    #    match='alias:code', params={'zonename': 'google.com'})

    # input answer from command line
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-M", "--method", help="specify which method to use")
    parser.add_option("-p", "--params", help="specify params for method")
    parser.add_option("-c", "--cached", help="specify using cache (y/n)")
    parser.add_option("-m", "--match",  help="specify match for method")
    (opts, args) = parser.parse_args()
    exec 'params = %s' % opts.params
    u.choose_method(method=opts.method, cached=opts.cached, match=opts.match, params=params)

