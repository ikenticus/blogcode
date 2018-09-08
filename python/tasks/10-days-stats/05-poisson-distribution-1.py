# Easy
# https://www.hackerrank.com/challenges/s10-poisson-distribution-1/problem

# http://ascii-table.com/html-table-greek-letters.php
# http://ascii-table.com/info.php?u=x03BB

# Poisson Experiment
'''
A Poisson experiment is a statistical experiment that has the following properties: 
* The outcome of each trial is either success or failure.
* The average number of successes (λ) that occurs in a specified region is known.
* The probability that a success will occur is proportional to the size of the region.
* The probability that a success will occur in an extremely small region is virtually zero. 
'''

# Poisson Distribution
'''
A Poisson random variable is the number of successes that result from a Poisson experiment. The probability distribution of a Poisson random variable is called a Poisson distribution:

             λ^k * e^-λ
    P(k,λ) = ----------
                 k!    

Here,
* e = 2.71828
* λ is the average number of successes that occur in a specified region.
* k is the actual number of successes that occur in a specified region.
* P(k,λ) is the Poisson probability, which is the probability of getting exactly k successes when the average number of successes is λ. 
'''

# Like all other distributions, if the question asks for more than or less than k, then the answer is the sum of r = 0..k or k..N

'''
Task 

A random variable, X, follows Poisson distribution with mean of 2.5. Find the probability with which the random variable X is equal to 5.

Input Format

The first line contains X's mean. The second line contains the value we want the probability for:

2.5
5

If you do not wish to read this information from stdin, you can hard-code it into your program.

Output Format

Print a single line denoting the answer, rounded to a scale of 3 decimal places (i.e., 1.234 format).
'''


# Enter your code here. Read input from STDIN. Print output to STDOUT
import math;

# poisson distribution
def p(k, l):
    return l**k * e**(-l) / math.factorial(k)

# combination function
def C(n, p):
    return math.factorial(n) / math.factorial(x) / math.factorial(n - x)

# input percentage, size of current batch
l = float(raw_input())
k = int(raw_input())

s = 3       # significance of answer
e = 2.71828

# poisson distribution
#print round(sum([p(x, l) for x in range(0, k + 1)]), s)
print round(p(k, l), s)
