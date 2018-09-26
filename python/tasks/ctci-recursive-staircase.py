#!/bin/python

import math
import os
import random
import re
import sys

# Complete the stepPerms function below.
dict = {0:0, 1:1, 2:2, 3:4}
def stepPerms(n):
    if n in dict.keys():
        return dict.get(n)
    result = stepPerms(n-3) + stepPerms(n-2) + stepPerms(n-1)
    dict.update({n: result})
    return dict.get(n)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = int(raw_input())

    for s_itr in xrange(s):
        n = int(raw_input())

        res = stepPerms(n)

        fptr.write(str(res) + '\n')

    fptr.close()

