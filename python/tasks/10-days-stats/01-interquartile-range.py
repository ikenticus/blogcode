# Easy 
# https://www.hackerrank.com/challenges/s10-interquartile-range

# Enter your code here. Read input from STDIN. Print output to STDOUT
N = int(raw_input())
X = [ int(i) for i in raw_input().rstrip().split(' ') ]
F = [ int(i) for i in raw_input().rstrip().split(' ') ]

# list comprehension
S = [ X[x] for x in range(len(X)) for _ in range(F[x]) ]
'''
S = []
for x in range(len(X)):
    for _ in range(F[x]):
        S.append(X[x])
'''

# sort, size
S.sort()
s = len(S)

# half size, offset, lists
hs = s/2
ho = hs % 2
h1 = S[:(s/2)]
h2 = S[(s+1)/2:]

Q1 = float((h1[(hs/2) + ho - 1] + h1[(hs+1)/2 - ho])) / 2
Q3 = float((h2[(hs/2) + ho - 1] + h2[(hs+1)/2 - ho])) / 2

print Q3 - Q1

