# Easy
# https://www.hackerrank.com/challenges/s10-binomial-distribution-2/problem

# A manufacturer of metal pistons finds that, on average, 12% of the pistons they manufacture are rejected because they are incorrectly sized. What is the probability that a batch of 10 pistons will contain:

* No more than 2 rejects?
* At least 2 rejects?

# Input Format
'''
A single line containing the following values (denoting the respective percentage of defective pistons and the size of the current batch of pistons):

12 10
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
import math;

# binomial probability mass function
def b(x, n, p):
    return C(n, x) * p**x * (1 - p)**(n - x)

# combination function
def C(n, p):
    return math.factorial(n) / math.factorial(x) / math.factorial(n - x)

# input percentage, size of current batch
P, n = list(map(float, raw_input().split(" "))) 

p = P / 100 # probability
r = 2       # number of rejects
s = 3       # significance of answer

# binomial distribution of at most 2 rejects
print round(sum([b(x, n, p) for x in range(0, r + 1)]), s)

# binomial distribution of at least 2 rejects
print round(sum([b(x, n, p) for x in range(r, int(n) + 1)]), s)
