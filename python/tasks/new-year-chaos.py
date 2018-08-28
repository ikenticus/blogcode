#!/bin/python

import math
import os
import random
import re
import sys

# Complete the minimumBribes function below.
def minimumBribes(q):
    '''
    # comparing and insert/pop times out
    line = [ i+1 for i in xrange(len(q)) ]
    bribes = 0
    for x in xrange(len(q)):
        init = line.index(q[x])
        moves = init - x
        if moves > 2:
            return 'Too chaotic'
            return
        if moves > 0:
            bribes += moves
            line.insert(x, line.pop(init))
    '''

    # bubble sorting more efficient
    last = len(q) - 1
    bribes = 0
    moved = False

    # more than 2 moves: Too chaotic
    for idx, pos in enumerate(q):
        if (pos - 1) - idx > 2:
            return "Too chaotic"

    # otherwise, execute bubble sort to count
    for i in xrange(0, last):
        for j in xrange(0, last):
            if q[j] > q[j+1]:
                q[j], q[j+1] = q[j+1], q[j]
                bribes += 1
                moved = True
        if not moved:
            break 
        moved = False

    return bribes

if __name__ == '__main__':
    t = int(raw_input())

    for t_itr in xrange(t):
        n = int(raw_input())

        q = map(int, raw_input().rstrip().split())

        print minimumBribes(q)
