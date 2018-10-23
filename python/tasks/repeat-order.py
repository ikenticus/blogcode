#!/usr/bin/python
'''

# Given a string of letters: AAABBC
# Rewrite it in the order they appear as: A3B2C

def process(s):
    pass

process('ABBCCC')
process('aAbBBBcCc')

'''


# initially tried to make a dictionary
# but that would mess up the 2nd 'cCc'

def process1(s):
    out = {}
    for i in s:
        if i in out:
            out[i] += 1
        else:
            out[i] = 1
    print out

process1('ABBCCC')
process1('aAbBBBcCc')


# next, switched up to making a string
# ugly, but eventually got working

def process2(s):
    cnt = 0
    out = ''
    for i in s:
        if out == '' or i != out[-1]:
            if cnt > 1:
                out += '%d' % cnt
            out += i
            cnt = 1
        else:
            cnt += 1
    if cnt > 1:
        out += '%d' % cnt
    print out

process2('ABBCCC')
process2('aAbBBBcCc')


