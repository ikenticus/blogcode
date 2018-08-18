'''
    Task: Chatroom
'''
import os
import sys
from operator import itemgetter

def usage():
    print 'Calculate the angle betwwen hour and minute hands\nUsage: %s <HH:MM>' % os.path.basename(sys.argv[0])

def degree (clock):
    hands = clock.split(':')
    min = 6 * int(hands[1])
    hour = int(hands[0])
    hour = (hour%12) * 30 + (min/12)
    return hour + 360 - min if (hour < min) else hour - min

# main
if len(sys.argv) < 1:
    usage()
    sys.exit(1)
print '%d degrees' % degree(sys.argv[1]);
