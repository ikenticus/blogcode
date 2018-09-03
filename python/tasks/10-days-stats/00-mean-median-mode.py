# Easy
# https://www.hackerrank.com/challenges/s10-basic-statistics/problem

# Enter your code here. Read input from STDIN. Print output to STDOUT
N = int(raw_input())
x = [ float(i) for i in raw_input().rstrip().split(' ') ]
x.sort()

n = {} # number hash
for c in range(len(x)):
    k = int(x[c]) # key
    if k in n.keys():
        n[k] += 1
    else:
        n[k] = 1
        
# mean
print '%.1f' % (sum(x) / len(x))

# median
print '%.1f' % ((x[len(x)/2 - 1] + x[(len(x) + 1)/2]) / 2)

# mode
print min([ m for m in n.keys() if n[m] == max(n.values()) ])

