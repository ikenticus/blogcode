import os
import sys
from pprint import pprint

phone = {
    2: "ABC",
    3: "DEF",
    4: "GHI",
    5: "JKL",
    6: "MNO",
    7: "PQRS",
    8: "TUV",
    9: "WXYZ"
}

marks = {
    "count": ['-', '=', '%', '#'],
    "shift": ['!', '@', '#', '$'],
    "ticks": ['', "'", '"', '-']
}

#pprint(phone)
#pprint(marks)

mark = os.getenv('MARK')
#print(marks[mark])

def encode(c, p):
    idx = phone[p].index(c)
    if mark and marks[mark]:
        return '%d%s ' % (p, marks[mark][idx])
    else:
        return '%s ' % (str(p) * (idx+1))
    
    
input = ''.join(sys.argv[1:]).upper()
#print(input)

output = ''
for c in input:
    for p in phone:
        #print("Checking %s against %d" % (c, p))
        if c in phone[p]:
            #print("%s will become %d" % (c, p))
            output += encode(c, p)
            continue

print(output)
