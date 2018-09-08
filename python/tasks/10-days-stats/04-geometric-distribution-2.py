# Easy
# https://www.hackerrank.com/challenges/s10-geometric-distribution-1/tutorial

# Negative Binomial Distribution
'''
A negative binomial experiment is a statistical experiment that has the following properties:

* The experiment consists of n repeated trials.
* The trials are independent.
* The outcome of each trial is either success (s) or failure (f).
* P(s) is the same for every trial.
* The experiment continues until x successes are observed. 

If X is the number of experiments until the xth success occurs, then X is a discrete random variable called a negative binomial. 

'''

# Negative Binomial Distribution
'''
Consider the following probability mass function:

                   (n - 1)    x   (n-x)
    b^*(x, n, p) = (x - 1) * p * q        =     C  * p^x * q^(n-x)
                                            n-1  x-1

The function above is negative binomial and has the following properties:
* The number of successes to be observed is x.
* The total number of trials is n.
* The probability of success of 1 trial is p.
* The probability of failure of 1 trial q, where 1 - p.
* b^*(x, n, p) is the negative binomial probability, meaning the probability of having x - 1 successes after n - 1 trials and having x successes after of n trials. 

Note: Recall that (n) = nCx:
                  (x)

          nPx         n!   
    nCx = --- = -------------
           x!   x! * (n - x)!
'''

# The probability that a machine produces a defective product is . What is the probability that the  defect is found during the  inspection?
'''
The first line contains the respective space-separated numerator and denominator for the probability of a defect, and the second line contains the inspection we want the probability of being the first defect for:

1 3
5

If you do not wish to read this information from stdin, you can hard-code it into your program.
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
import math;

# negative binomial probability mass function
def bn(x, n, p):
    return C(n - 1, x - 1) * p**x * (1 - p)**(n - x)

# binomial probability mass function
def b(x, n, p):
    return C(n, x) * p**x * (1 - p)**(n - x)


# combination function
def C(n, p):
    if (n - x) < 0:
        return 1
    return math.factorial(n) / math.factorial(x) / math.factorial(n - x)

# input ratio: probability of a defect, numerator and denominator 
R = list(map(float, raw_input().split(" ")))
p = R[0] / R[1]

n = int(raw_input())    # number of inspections
s = 3                   # significance of answer

# negative binomial distribution of n inspections
print round(sum([b(x, n, p) for x in range(1, n + 1)]), s)

