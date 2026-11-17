import os
import sys
from pprint import pprint

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#pprint(alpha)

shift = int(os.getenv('SHIFT', '0'))
#print(shift)

key = os.getenv('KEY')
if not key:
    crypt = alpha[shift:] + alpha[0:shift]
else:
    if len(set(key)) != len(key):
        print('Key must not have repeating letters: %s' % ''.join(set(key)))
        sys.exit(0)
    else:
        beta = alpha[shift:] + alpha[0:shift]
        for k in key.upper():
            beta = beta.replace(k, '', 1) 
        crypt = key.upper() + beta
#print(crypt)

input = ''.join(sys.argv[1:]).upper()
#print(input)

decode = os.getenv('DECODE')
output = ''
for c in input:
    if not decode:
        #print('Converting %s to %s' % (c, crypt[alpha.index(c)]))
        output += crypt[alpha.index(c)]
    else:
        output += alpha[crypt.index(c)]
        
print(output)
