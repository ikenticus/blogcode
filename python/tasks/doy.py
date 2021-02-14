import os
import sys
from datetime import datetime as dt

file = os.path.basename(sys.argv[0]).replace('.py', '.txt')
data = open(file).read().rstrip().split('\n')

max = None
if len(sys.argv) > 1:
    max = int(sys.argv[1])

extra = None
if len(sys.argv) > 2:
    extra = int(sys.argv[2])

sid = 86400
anchor = dt.strptime('2000/01/01', '%Y/%m/%d').strftime('%s')
for day in data:
    secs = dt.strptime('2000/' + day, '%Y/%m/%d').strftime('%s')
    doy = int( (int(secs) - int(anchor)) / sid ) + 1
    if max:
        print('%d\t%s' % (int(doy / 365 * max), day))
    else:
        print(doy)
if extra:
    print('X:%d\tBonus' % int(7 / 12 * extra))

