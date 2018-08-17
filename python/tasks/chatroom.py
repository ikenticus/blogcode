'''
    Task: Chatroom
'''
import os
import sys
from operator import itemgetter

def usage():
    print 'Display chatroom statistics\nUsage: %s <chatfile> <n>' % os.path.basename(sys.argv[0])

def parse (data):
    stat = {}
    lines = data.split('\n')
    for c in lines:
        if len(c) > 0:
            s = c.split(':', 2)
            user = s[0].strip()
            chat = s[1].strip()

            if user not in stat.keys():
                stat[user] = {
                    'Words': []
                }
            stat[user]['Words'].extend(chat.split(' '))
            stat[user]['Count'] = len(stat[user]['Words'])
    return stat

def output (order, stat):
    most = not(order.startswith('-'))
    mostWord = 'most' if most else 'least'
    rank = abs(int(order))

    user = [ {'Name': k, 'Count': stat[k]['Count']} for k in stat ]
    user = sorted(user, key=itemgetter('Count'), reverse=most)

    if rank == 0:
        print 'List of %s wordy users:' % mostWord
        for u in user:
            print '%5d %s' % (u['Count'], u['Name'])
    else:
        # https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
        print 'The %d%s %s wordy user is (%s) with %d words' % (
            rank, "tsnrhtdd"[(rank/10%10!=1)*((rank%10)<4)*(rank%10)::4],
            mostWord, user[rank-1]['Name'], user[rank-1]['Count'])

# main
if len(sys.argv) < 3:
    usage()
    sys.exit(1)

chatfile = sys.argv[1]
data = open(chatfile, 'r').read()
stat = parse(data)
output(sys.argv[2], stat)
