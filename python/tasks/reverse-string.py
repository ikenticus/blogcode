
# Write a quick function to reverse a string without built-in reverse function

import sys

def reverse(str):
    newstring = []
    for s in range(len(str)-1, -1, -1):
        newstring.append(str[s])
    return ''.join(newstring)

print(reverse(sys.argv[1]))

# What is the Big-O notation: O(n)
# How can we reduce that: divide len in half and process front/back simultaneously
# What is the Big-O: O(n/2) if using half len(), but still O(n) since constants omitted

def reverse2(str):
    newstring = list(str)
    for s in range(0, round(len(str)/2)):
        end = len(str) - s - 1
        newstring[end] = str[s]
        newstring[s] = str[end]
    return ''.join(newstring)

print(reverse2(sys.argv[1]))
