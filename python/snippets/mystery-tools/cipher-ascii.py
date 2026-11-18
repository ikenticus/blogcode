import os
import sys
from pprint import pprint

sep = os.getenv('SEP', ' ')

input = ''.join(sys.argv[1:])
#print(input)

decode = os.getenv('DECODE')
output = ''
if not decode:
    for c in input:
        output += '%d%s' % (ord(c), sep)
else:
    for i in input.split(sep):
        if i:
            output += chr(int(i))

print(output)
