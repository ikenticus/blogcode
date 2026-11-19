import os
import sys
from pprint import pprint

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

sep = os.getenv('SEP', ' ')

input = ''.join(sys.argv[1:]).upper()
#print(input)

decode = os.getenv('DECODE')
output = ''
if not decode:
    for c in input:
        output += '%d%s' % (alpha.index(c) + 1, sep)
else:
    for i in input.split(sep):
        if i:
            output += alpha[int(i)-1]
        
output = output.rstrip(sep)
print(output)
