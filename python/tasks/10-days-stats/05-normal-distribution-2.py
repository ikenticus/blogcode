# Easy
# https://www.hackerrank.com/challenges/s10-normal-distribution-2/problem

'''
Task 

The final grades for a Physics exam taken by a large group of students have a mean of mu = 70 and a standard deviation of sd = 10. If we can approximate the distribution of these grades by a normal distribution, what percentage of the students:

1. Scored higher than 80 (i.e., have a grade >= 80)?
2. Passed the test (i.e., have a grade >= 60)?
3. Failed the test (i.e., have a grade < 60)?

Find and print the answer to each question on a new line, rounded to a scale of 2 decimal places.

Input Format

There are 3 lines of input (shown below):

70 10
80
60

The first line contains 2 space-separated values denoting the respective mean and standard deviation for the exam. The second line contains the number associated with question 1. The third line contains the pass/fail threshold number associated with questions 2 and 3.

If you do not wish to read this information from stdin, you can hard-code it into your program.

Output Format

15.87
84.13
15.87

There are three lines of output. Your answers must be rounded to a scale of 2 decimal places (i.e., 1.23 format):

On the first line, print the answer to question 1 (i.e., the percentage of students having grade > 80).
On the second line, print the answer to question 2 (i.e., the percentage of students having grade >= 60).
On the third line, print the answer to question 3 (i.e., the percentage of students having grade < 60).
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
x1 = float(raw_input())    # number associated with question 1
x2 = float(raw_input())    # number associated with question 2,3

s = 2   # significance

A1 = 100 - 100 * Phi(x1, mu, sd)
print round(A1, s)

A3 = 100 * Phi(x2, mu, sd)
A2 = 100 - A3
print round(A2, s)
print round(A3, s)
