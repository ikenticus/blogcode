import datetime
import os
import sys

if len(sys.argv) > 1:
    ask = sys.argv[1]
    try:
        testDate = datetime.datetime(*tuple([int(a) for a in ask.split('-')]))
        correctDate = True
    except ValueError:
        correctDate = False
    print('%s is Valid? %s' % (ask, str(correctDate)))
else:
    print('Usage: %s yyyy-mm-dd' % os.path.basename(sys.argv[0]))

