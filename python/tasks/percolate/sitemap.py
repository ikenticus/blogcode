'''
    code review was done on company laptop so this problem is not verbatim
    but is a reconstruction based on my memory several hours after the fact

    given the following list of urls:

    example_input = (
        'percolate/uri/1',
        'expresso/path/1',
        'expresso/path/2',
        'coffee',
    )

    create a sitemap with the urls like:

    example_output = {
        "percolate": {
            "uri: {"1": {}}
        },
        "expresso": {
            "path": {
                "1": {},
                "2": {}
            }
        },
        "coffee": {}
    }
'''

#def sitemap(_input):


'''
    first attempt followed by pretty-print alteration, subsequently json.dumps
'''

import json
from pprint import pprint

def sitemap(_input):
    output = {}
    for i in _input:
        ptr = output
        for p in i.split('/'):
            if p not in ptr:
                ptr[p] = {}
            ptr = ptr[p]
    return output

example_input = (
    'percolate/uri/1',
    'expresso/path/1',
    'expresso/path/2',
    'coffee',
)

example_output = sitemap(example_input)
pprint(example_output, indent=2)
print json.dumps(example_output, indent=2)
