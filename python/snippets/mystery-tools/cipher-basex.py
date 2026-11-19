import os
import sys
from pprint import pprint

sep = os.getenv('SEP', ' ')
base = int(os.getenv('BASE', '2'))

if base > 10 and base != 16:
    print("The only base > 10 supported is 16, AKA hexadecimal")
    sys.exit(1)

def encode(n: int) -> str:
    if n == 0:
        return "0"
    
    sign = "-" if n < 0 else ""
    n = abs(n)
    digits = []
    
    while n > 0:
        n, remainder = divmod(n, base)
        digits.append(str(remainder))
        
    return sign + "".join(reversed(digits))

input = ''.join(sys.argv[1:])
#print(input)

decode = os.getenv('DECODE')
output = ''
for i in input.split(sep):
    if not decode:
        print(i)
        if base == 16:
            d = int(i)
            output += '%s%s' % (f"{d:X}", sep)
        else:
            output += '%s%s' % (encode(int(i)), sep)
        output = output.rstrip(sep)
    else:
        if base == 16:
            if i:
                output += '%s%s' % (int(i, base), sep)
        else:
            valid = False
            for c in i:
                valid = True if int(c) < base else False 
            if valid:
                output += '%s%s' % (int(i, base), sep)
            else:
                print("In base%d decoding, all digits must be less than %d" % (base, base))
                sys.exit(1)

print(output)
