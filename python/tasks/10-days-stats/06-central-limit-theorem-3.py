# Easy
# https://www.hackerrank.com/challenges/s10-the-central-limit-theorem-2/problem

# Confidence Level 
'''
Typical two sided confidence levels are:
     C	      z*
    99%	    2.576
    98%	    2.326
    95%	    1.96
    90%	    1.645

The confidence interval is then calculated by:

                                             sd             sd
For a known standard deviation:     mu - z ------- , mu + -------
                                           sqrt(n)        sqrt(n)

                                              s                s
For an unknown standard deviation:  mu - t ------- , mu + t -------
                                           sqrt(n)          sqrt(n)

'''

'''
Objective 

In this challenge, we practice solving problems based on the Central Limit Theorem. We recommend reviewing the Central Limit Theorem Tutorial before attempting this challenge.

Task 

You have a sample of  values from a population with mean mu = 500 and with standard deviation sd = 80. Compute the interval that covers the middle 95% of the distribution of the sample mean; in other words, compute A and B such that P(A < x < B). Use the value of z=1.96. Note that z is the z-score.

Input Format

There are five lines of input (shown below):

100
500
80
.95
1.96

The first line contains the sample size. The second and third lines contain the respective mean (mu) and standard deviation (sd). The fourth line contains the distribution percentage we want to cover (as a decimal), and the fifth line contains the value of z.

If you do not wish to read this information from stdin, you can hard-code it into your program.

Output Format

Print the following two lines of output, rounded to a scale of 3 decimal places (i.e., 1.23 format):

On the first line, print the value of A.
On the second line, print the value of B.
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
import math

# cumulative distribution function
def Phi(x, mu, sd):
    return (1 + math.erf((x - mu) / sd / math.sqrt(2))) / 2

# confidence interval
def CI(mu, sd, z, n)
    return mu + z * sd / math.sqrt(n)

n = int(raw_input())
mu = int(raw_input())
sd = int(raw_input())
p = float(raw_input())
z = float(raw_input())

s = 3   # significance

print round(CI(mu, sd, -z, n), s)
print round(CI(mu, sd, z, n), s)

