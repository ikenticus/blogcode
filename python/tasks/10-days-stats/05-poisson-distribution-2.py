# Easy
# https://www.hackerrank.com/challenges/s10-poisson-distribution-2/problem

# Special Case
'''
Consider some Poisson random variable, X. Let E[X] be the expectation of X. Find the value of E[X2]. 


Let Var(X) be the variance of X. Recall that if a random variable has a Poisson distribution, then: 

* E[X] = λ
* Var(X) = λ

Now, we'll use the following property of expectation and variance for any random variable, X:

    Var(X) = E[X^2] - (E[X])^2
        =>   E[X^2] = Var(X) + (E[X])^2

So, for any random variable X having a Poisson distribution, the above result can be rewritten as:

        =>   E[X^2] = λ + λ^2

'''

# http://ascii-table.com/html-table-greek-letters.php
# http://ascii-table.com/info.php?u=x03BB

'''
Task 

The manager of a industrial plant is planning to buy a machine of either type A or type B. For each day’s operation:

* The number of repairs, X, that machine A needs is a Poisson random variable with mean 0.88. The daily cost of operating A is Ca = 160 + 40X^2.
* The number of repairs, Y, that machine B needs is a Poisson random variable with mean 1.55. The daily cost of operating B is Cb = 128 + 40Y^2.

Assume that the repairs take a negligible amount of time and the machines are maintained nightly to ensure that they operate like new at the start of each day. Find and print the expected daily cost for each machine.

Input Format

A single line comprised of 2 space-separated values denoting the respective means for A and B:

0.88 1.55

If you do not wish to read this information from stdin, you can hard-code it into your program.

Output Format

There are two lines of output. Your answers must be rounded to a scale of 3 decimal places (i.e., 1.234 format):

On the first line, print the expected daily cost of machine A.
On the second line, print the expected daily cost of machine B.
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
Lx, Ly = list(map(float, raw_input().split(" ")))

s = 3       # significance of answer
e = 2.71828

# Cost
Cx = 160 + 40 * (Lx + Lx**2)
Cy = 128 + 40 * (Ly + Ly**2)

print(round(Cx, s))
print(round(Cy, s))
