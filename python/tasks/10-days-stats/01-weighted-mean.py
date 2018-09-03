# Easy
# https://www.hackerrank.com/challenges/s10-weighted-mean/problem

# Enter your code here. Read input from STDIN. Print output to STDOUT
N = int(raw_input())
X = [ float(i) for i in raw_input().rstrip().split(' ') ]
W = [ int(i) for i in raw_input().rstrip().split(' ') ]

num = []
for i in range(len(X)):
    num.append(X[i] * W[i])

# weighted mean
print '%.1f' % (sum(num) / sum(W))


