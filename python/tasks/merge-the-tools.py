# Medium
# https://www.hackerrank.com/challenges/merge-the-tools/problem

# Misunderstodd and divided the strings into k strings,
# not strings of k length, so only passed Testcase0
'''
def merge_the_tools(string, k):
    # your code goes here
    s = len(string) / k
    for t in range(0, len(string), s):
        u = ''
        for x in string[t:t+s]:
            if x not in u:
                u += x
        print u
'''

def merge_the_tools(string, k):
    # your code goes here
    for t in range(0, len(string), k):
        u = ''
        for x in string[t:t+k]:
            if x not in u:
                u += x
        print u


if __name__ == '__main__':
    string, k = raw_input(), int(raw_input())
    merge_the_tools(string, k)
    

'''
Testcase0: 
AABCAAADA
3

Output0:
AB
CA
AD


Testcase1:
<< merge-the-tools-testcase1.txt

Output1:
KYQTWXDLINFBHRGZVCUSAMOEPJ
YUGTZIWNVSALBXOCDMPFEKJRQH
'''
