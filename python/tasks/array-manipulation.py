#!/bin/python

import math
import os
import random
import re
import sys

# Complete the arrayManipulation function below.
def arrayManipulation(n, queries):

    '''
    # this method times out with 10k queries
    arr = [ 0 for i in xrange(n) ]
    for q in queries:
        a, b, k = q
        for i in xrange(a, b + 1):
            arr[i-1] += k
    return max(arr)
    '''
    # https://codereview.stackexchange.com/questions/95755/algorithmic-crush-problem-hitting-timeout-errors
    arr = [ 0 for i in xrange(n+1) ]
    for q in queries:
        a, b, k = q
        # calculate differance array
        arr[a-1] += k
        arr[b] -= k
    max = 0
    sum = 0
    for i in arr:
        # determine max using prefix sum
        sum += i
        if sum > max:
            max = sum
    return max

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nm = raw_input().split()

    n = int(nm[0])

    m = int(nm[1])

    queries = []

    for _ in xrange(m):
        queries.append(map(int, raw_input().rstrip().split()))

    result = arrayManipulation(n, queries)

    fptr.write(str(result) + '\n')

    fptr.close()

