#!/bin/python

import math
import os
import random
import re
import sys

# use this function to complete the task
def task(n, queries):
    print n, queries
    return 1

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nm = raw_input().split()

    n = int(nm[0])

    m = int(nm[1])

    queries = []

    for _ in xrange(m):
        queries.append(map(int, raw_input().rstrip().split()))

    result = task(n, queries)

    fptr.write(str(result) + '\n')

    fptr.close()

'''
# Stdin
5 3
1 2 100
2 5 100
3 4 100

'''
