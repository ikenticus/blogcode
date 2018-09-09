# Easy
# https://www.hackerrank.com/challenges/s10-least-square-regression-line/problem

'''
Objective 

In this challenge, we practice using linear regression techniques. Check out the Tutorial tab for learning materials!

Task 

A group of five students enrolls in Statistics immediately after taking a Math aptitude test. Each student's Math aptitude test score, x, and Statistics course grade, y, can be expressed as the following list of (x, y) points:

1. (85, 85)
2. (85, 96)
3. (80, 70)
4. (70, 65)
5. (60, 70)

If a student scored an 80 on the Math aptitude test, what grade would we expect them to achieve in Statistics? Determine the equation of the best-fit line using the least squares method, then compute and print the value of y when x = 80.

Input Format

There are five lines of input; each line contains two space-separated integers describing a student's respective  and  grades:

95 85
85 95
80 70
70 65
60 70

If you do not wish to read this information from stdin, you can hard-code it into your program.

Output Format

Print a single line denoting the answer, rounded to a scale of 3 decimal places (i.e., 1.234 format).
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
s = 3   # significance
N = 5   # number of grades

X, Y = [], []
for i in range(N):
    # [int(i) for i in raw_input().split()]
    x, y = list(map(int, raw_input().rstrip().split(" ")))
    X.append(x)
    Y.append(y)

mx = sum(X) / N
my = sum(Y) / N
X2 = sum([ X[i]**2 for i in range(N) ])
XY = sum([ X[i] * Y[i] for i in range(N) ])


# Coefficient of Determination (R-squared)
b = 1.0 * (N * XY - sum(X) * sum(Y)) / (N * X2 - sum(X)**2)
a = my - b * mx

print round(a + b*80, s)

'''
Testcase0: 78.288
95 85
85 95
80 70
70 65
60 70
'''
