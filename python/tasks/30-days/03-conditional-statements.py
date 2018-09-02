#!/bin/python

import math
import os
import random
import re
import sys

if __name__ == '__main__':
    N = int(raw_input())
    if N % 2 == 1 or (N >= 6 and N <= 20):
        print 'Weird'
    else:
        print 'Not Weird'

