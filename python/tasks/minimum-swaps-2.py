#!/bin/python

import math
import os
import random
import re
import sys

# Complete the minimumSwaps function below.
def minimumSwaps(arr):
    ord = arr[:]
    ord.sort()
    swaps = 0
    while arr != ord:
        # extract unsorted items first
        mix = []
        for i in range(0, len(arr)):
            if arr[i] != ord[i]:
                mix.append(arr[i])
        arr = mix[:]
        ord = mix[:]
        ord.sort()

        # then figure out swaps from reduced list
        for i in range(0, len(arr)):
            a = arr[i]
            if a != ord[i]:
                swaps += 1
                j = ord.index(a)
                arr[i] = arr[j]
                arr[j] = a

        # while this two-pronged method in node.js
        # still times out in python2 on 100k array
    return swaps

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(raw_input())

    arr = map(int, raw_input().rstrip().split())

    res = minimumSwaps(arr)

    fptr.write(str(res) + '\n')

    fptr.close()
