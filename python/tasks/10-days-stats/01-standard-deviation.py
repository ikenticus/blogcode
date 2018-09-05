# Easy
# https://www.hackerrank.com/challenges/s10-standard-deviation

# Enter your code here. Read input from STDIN. Print output to STDOUT
N = int(raw_input())
X = [ int(i) for i in raw_input().rstrip().split(' ') ]

mu = float(sum(X)) / N
S = sum([ (x - mu) ** 2 for x in X ])
sd = (S / N) ** 0.5

print '%.1f' % sd

