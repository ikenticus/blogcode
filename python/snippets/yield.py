#!/bin/python

import sys

def check(nums, num):
    for n in nums:
        if n % num == 0:
            yield(n)

if __name__ == '__main__':
    nums = [n for n in range(100)]
    for n in check(nums, int(sys.argv[1])):
        print n

