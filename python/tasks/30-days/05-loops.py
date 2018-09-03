#!/bin/python

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    n = int(raw_input())
    for i in range(1, 11):
        print '%d x %d = %d' % (n, i, n * i)

