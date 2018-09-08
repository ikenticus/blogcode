# Easy
# https://www.hackerrank.com/challenges/s10-normal-distribution-1/problem

'''
Objective 

In this challenge, we learn about normal distributions. Check out the Tutorial tab for learning materials!

Task 

In a certain plant, the time taken to assemble a car is a random variable, X, having a normal distribution with a mean of hours and a standard deviation of 2 hours. What is the probability that a car can be assembled at this plant in:

1. Less than 19.5 hours?
2. Between 20 and 22 hours?

Input Format

There are 3 lines of input (shown below):

20 2
19.5
20 22

The first line containsa2  space-separated values denoting the respective mean and standard deviation for X. The second line contains the number associated with question 1. The third line contains 2 space-separated values describing the respective lower and upper range boundaries for question 2.

If you do not wish to read this information from stdin, you can hard-code it into your program.

Output Format

There are two lines of output. Your answers must be rounded to a scale of 3 decimal places (i.e., 1.234 format):

On the first line, print the answer to question 1 (i.e., the probability that a car can be assembled in less than 19.5 hours).
On the second line, print the answer to question 2 (i.e., the probability that a car can be assembled in between 20 to 22 hours).
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
import math;

# normal distribution
def N(x, mu, v):
    return math.e**-((x - mu)**2 / 2 / v) / math.sqrt(2 * math.pi * v)

# standard normal distribution
def phi(x):
    return math.e**-(x**2 / 2) / math.sqrt(2 * math.pi)

# cumulative distribution function
def Phi(x, mu, sd):
    return (1 + math.erf((x - mu) / sd / math.sqrt(2))) / 2

mu, sd = list(map(float, raw_input().split(" ")))
x1 = int(raw_input())    # number associated with question 1
x2 = list(map(int, raw_input().split(" ")))

s = 3   # significance

A1 = Phi(x1, mu, sd)
print round(A1, s)

A2 = Phi(x2[1], mu, sd) - Phi(x2[0], mu, sd)
print round(A2, s)
