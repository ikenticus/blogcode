# coderbyte exercise:
# Implement `map` using `reduce`

# https://docs.python.org/3/library/functions.html#map#
# https://docs.python.org/3/library/functools.html#functools.reduce
# def map(func, items) -> list: pass

# def map(func, items) -> list: pass
#   return functools.reduce(func, items)
#
# def add_one(x):
#   print(x)
#
# map(add_one, [1,2,3])
#
# # Run code:
# (1, 2)
# (None, 3)
# (None, 4)
# (None, 5)
# (None, 6)

# From this output, I finally realized that reduce does the following:
# - 1. takes the first pair and passes it to the func
# - 2. pass the result of that pair with the next item to the func
# - 3. repeats until it exhausts the iterations

# Eventually, once I figured that out, he stopped me for time

import functools
import sys

def map1(func, items) -> list:
    return functools.reduce(func, list(items))

def add1(*items):
    # sum is incorrect, only returns final item and not mapped list
    # return sum([ int(i) for i in list(items) ])
    if isinstance(items[0], str):
        memo = [int(items[0]) + 1]
    elif isinstance(items[0], int):
        memo = [items[0] + 1]
    elif isinstance(items[0], list):
        memo = items[0]
    else:
        memo = []
    return memo + [int(items[1]) + 1]

print(map1(add1, sys.argv[1:]))

# _.reduce(list, iteratee, [memo], [context])
# The memo will be the initial state of the return value.
# For every element of your list, the memo is given to the iteratee function,
# where it's expected to be modified and returned.

# Use the reduce function to build the map function
# functools.reduce(function, iterable[, initializer])
from functools import reduce

def map2(fn, array):
    return reduce(fn, array, [])

def add2(memo, num):
    memo.append(int(num) + 2)
    return memo

print(map2(add2, sys.argv[1:]))

# What if user is unaware we are using reduce, how can they simply add with 1 param?

def map3(fn, array):
    def wrapper_fn(memo, num):
        memo.append(fn(num))
        return memo
    return reduce(wrapper_fn, array, [])

def add3(num):
    return int(num) + 3

print(map3(add3, sys.argv[1:]))
