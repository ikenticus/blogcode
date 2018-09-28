'''
    reader: contains all the function used to parse and organize data file
'''
import config
import json
import os
import re

def parse(line):
    '''
        parse each line and compare with valid_line pattern in config
    '''
    entry = {}
    for valid in config.valid_lines:
        check = valid['patt'].match(line)
        if check:
            for item in valid['list']:
                idx = valid['list'].index(item) + 1
                if item.startswith('phone'):
                    if item == 'phonenumber':
                        entry[item] = '-'.join(check.group(idx, idx+1, idx+2))
                else:
                    entry[item] = check.group(idx)
    return entry

def read(filename):
    '''
        read data input file and create rolodex json
    '''
    idx = 0
    output = {
        'entries': [],
        'errors': []
    }
    with open(filename, 'r') as lines:
        for line in lines:
            entry = parse(line.rstrip())
            if entry:
                output['entries'].append(entry)
            else:
                output['errors'].append(idx)
            idx += 1
    return output

def write(output, filename):
    '''
        sort and write the corresponding output json file
    '''
    output['entries'].sort(key=lambda x: (x['lastname'], x['firstname']))
    data = json.dumps(output, sort_keys=True, indent=2)
    with open(filename, 'w+') as out:
        out.write(data)
