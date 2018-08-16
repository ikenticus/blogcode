'''
    Task: Fibonacci
'''
import os
import sys

def usage():
    print 'Calculate the Nth Fibonacci number\nUsage: %s <n>' % os.path.basename(sys.argv[0])

SEQ = [ 0, 1 ]
if len(sys.argv) == 1:
    usage()
    sys.exit(1)
elif int(sys.argv[1]) <= 1:
    print 'F(%s) = %s' % (sys.argv[1], sys.argv[1])
    if int(sys.argv[1]) < 1:
        del SEQ[1]
else:
    NUM = int(sys.argv[1])
    # cannot use list comprehension because it needs to index dynamically
    #SEQ.extend([ SEQ[i - 1] + SEQ[i - 2] for i in range(0, NUM) if NUM > 1 ])
    if NUM > 1:
        for i in range(2, NUM+1):
            SEQ.append(SEQ[i-1] + SEQ[i-2])
    SIZE = len(SEQ) - 1
    print 'F(%d) = %d' % (NUM, SEQ[SIZE])
print 'Sequence:', SEQ
