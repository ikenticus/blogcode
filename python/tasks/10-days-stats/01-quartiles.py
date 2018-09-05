# Easy
# https://www.hackerrank.com/challenges/s10-quartiles

# Enter your code here. Read input from STDIN. Print output to STDOUT
N = int(raw_input())
x = [ int(i) for i in raw_input().rstrip().split(' ') ]

# sort, size, offset for odd/even
x.sort()
s = len(x)
o = s % 2

# half size, offset, lists
hs = s/2
ho = hs % 2
h1 = x[:(s/2)]
h2 = x[(s+1)/2:]

Q1 = (h1[(hs/2) + ho - 1] + h1[(hs+1)/2 - ho]) / 2
Q2 = (x[(s/2) + o - 1] + x[(s+1)/2 - o]) / 2
Q3 = (h2[(hs/2) + ho - 1] + h2[(hs+1)/2 - ho]) / 2

print Q1    #, h1, (hs/2) + ho - 1, (hs+1)/2 - ho
print Q2    #, ho, hs
print Q3    #, h2, (hs/2) + ho - 1, (hs+1)/2 - ho

