#!/bin/python

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    n = int(raw_input())

    arr = map(int, raw_input().rstrip().split())
    print ' '.join([ str(arr[len(arr)-i-1]) for i in range(len(arr)) ])
        
