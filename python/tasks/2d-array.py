#!/bin/python

import math
import os
import random
import re
import sys

# Complete the hourglassSum function below.
def hourglassSum(arr):
    hours = []
    for r in range(len(arr) - 2):
        for c in range(len(arr[r]) - 2):
            hours.append([
                arr[r][c], arr[r][c+1], arr[r][c+2],
                            arr[r+1][c+1],
                arr[r+2][c], arr[r+2][c+1], arr[r+2][c+2]
                ])
    
    sums = []
    for h in hours:
        sums.append(sum(h))

    return max(sums)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    arr = []

    for _ in xrange(6):
        arr.append(map(int, raw_input().rstrip().split()))

    result = hourglassSum(arr)

    fptr.write(str(result) + '\n')

    fptr.close()

