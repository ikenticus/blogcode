# Easy
# https://www.hackerrank.com/challenges/s10-binomial-distribution-1/problem

# Binomial Distribution
'''
We define a binomial process to be a binomial experiment meeting the following conditions: 

* The number of successes is x.
* The total number of trials is n.
* The probability of success of 1 trial is p.
* The probability of failure of 1 trial q, where 1 - p.
* b(x, n, p) is the binomial probability, meaning the probability of having exactly x successes out of n trials. 

The binomial random variable is the number of successes, x, out of n trials. 


The binomial distribution is the probability distribution for the binomial random variable, given by the following probability mass function:

                 (n)    x   (n-x)
    b(x, n, p) = (x) * p * q        = nCx * p^x * q^(n-x)

Note: Recall that (n) = nCx:
                  (x)

          nPx         n!   
    nCx = --- = -------------
           x!   x! * (n - x)!
'''

# The ratio of boys to girls for babies born in Russia is 1.09 : 1. If there is 1 child born per birth, what proportion of Russian families with exactly 6 children will have at least 3 boys?

# Write a program to compute the answer using the above parameters. Then print your result, rounded to a scale of 3 decimal places (i.e., 1.234 format).

# Enter your code here. Read input from STDIN. Print output to STDOUT
import math;

# binomial probability mass function
def b(x, n, p):
    return C(n, x) * p**x * (1 - p)**(n - x)

# combination function
def C(n, p):
    return math.factorial(n) / math.factorial(x) / math.factorial(n - x)

# input ratio: boys girls
R = list(map(float, raw_input().split(" ")))

# probability of boys / children
p = R[0] / sum(R)

n = 6   # number of children born
r = 3   # number of boys
s = 3   # significance of answer

# binomial distribution of at least 3 boys out of 6 children
print round(sum([b(x, n, p) for x in range(r, n + 1)]), s)

