# Easy
# https://www.hackerrank.com/challenges/s10-geometric-distribution-1

# Geometric Distribution
'''
The geometric distribution is a special case of the negative binomial distribution that deals with the number of Bernoulli trials required to get a success (i.e., counting the number of failures before the first success). Recall that X is the number of successes in n independent Bernoulli trials, so for each i (where 1 <= i <= n):

          { 1   if the ith trial is a success
    Xi = {
          { 0   otherwise

The geometric distribution is a negative binomial distribution where the number of successes is . We express this with the following formula:

    g(n, p) = q^(n-1) * p

'''

# Example
'''
Bob is a high school basketball player. He is a 70% free throw shooter, meaning his probability of making a free throw is 0.7. What is the probability that Bob makes his first free throw on his fifth shot? 

For this experiment, n = 5, p = 0.7 and q = 0.3, So, g(n = 5, p = 0.7) = 0.3^4 * 0.7 = 0.00567

'''

# The probability that a machine produces a defective product is . What is the probability that the  defect is found during the  inspection?
# The first line contains the respective space-separated numerator and denominator for the probability of a defect, and the second line contains the inspection we want the probability of being the first defect for:
'''
1 3
5
'''
# Print a single line denoting the answer, rounded to a scale of  decimal places (i.e.,  format).

# Enter your code here. Read input from STDIN. Print output to STDOUT
import math;

# geometric probability
def g(n, p):
    return p * (1 - p)**(n - 1)

# input ratio: probability of a defect, numerator and denominator 
R = list(map(float, raw_input().split(" ")))
p = R[0] / R[1]

n = int(raw_input())    # number of inspections
s = 3                   # significance of answer

# geometric distribution of n inspections
print round(g(n, p), s)

