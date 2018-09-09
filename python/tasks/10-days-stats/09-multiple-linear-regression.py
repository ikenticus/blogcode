# Medium
# https://www.hackerrank.com/challenges/s10-multiple-linear-regression/problem

'''
Objective 

In this challenge, we practice using multiple linear regression. Check out the Tutorial tab for learning materials!

Task 

Andrea has a simple equation:

    Y = a + b1 * f1 + b1 * f2 + ... + bm * fm

for (m + 1) real constants (a, f1, f2, ..., fm). We can say that the value of Y depends on m features. Andrea studies this equation for n different feature sets (f1, f2, f3, ..., fm) and records each respective value of Y. If she has q new feature sets, can you help Andrea find the value of Y for each of the sets?

Note: You are not expected to account for bias and variance trade-offs.

Input Format

The first line contains 2 space-separated integers, m (the number of observed features) and n (the number of feature sets Andrea studied), respectively. 
Each of the n subsequent lines contain m + 1 space-separated decimals; the first m elements are features (f1, f2, f3, ..., fm), and the last element is the value of Y for the line's feature set.
The next line contains a single integer, q, denoting the number of feature sets Andrea wants to query for. 
Each of the q subsequent lines contains m space-separated decimals describing the feature sets.

Constraints

  1 <= m <= 10
  5 <= n <= 100
  0 <= xi <= 1
  0 <= Y <= 10^6
  1 <= q <= 100

Scoring

For each feature set in one test case, we will compute the following:

        |Computed value of Y - Expected value of Y|
* di' = -------------------------------------------
                     Expected value of Y           

* di = max(di' - 0.1, 0). We will permit up to a +-10% margin of error.
* si = max(1.0 - di, 0)

The normalized score for each test case will be: S = Sum(i = 1, q) si / q. If the challenge is worth C points, then your score will be S x C.

Output Format

For each of the q feature sets, print the value of Y on a new line (i.e., you must print a total of q lines).

Sample Input

2 7
0.18 0.89 109.85
1.0 0.26 155.72
0.92 0.11 137.66
0.07 0.37 76.17
0.85 0.16 139.75
0.99 0.41 162.6
0.87 0.47 151.77
4
0.49 0.18
0.57 0.83
0.56 0.64
0.76 0.18

Sample Output

105.22
142.68
132.94
129.71

Explanation

We're given m = 2, so iY = a + b1 * f1 + b2i * f2. We're also given n = 7, so we determine that Andrea studied the following feature sets:

    a + 0.18 b1 + 0.89 b2 = 109.85
    a + 1.0 b1 + 0.26 b2 = 115.72
    a + 0.92 b1 + 0.11 b2 = 137.66
    a + 0.07 b1 + 0.37 b2 = 76.17
    a + 0.85 b1 + 0.16 b2 = 139.75
    a + 0.99 b1 + 0.41 b2 = 162.6
    a + 0.87 b1 + 0.47 b2 = 151.77

We use the information above to find the values of a, b1, and b2. Then, we find the value of Y for each of the q feature sets.
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
import numpy

FY = {}
m, n = list(map(int, raw_input().rstrip().split(" ")))
# use numpy to solve for a, b1, ..., bm

# FY = [ f1, ..., fm, Y]
FY = numpy.array([raw_input().rstrip().split(" ") for _ in range(n)], float)

# F = [ f1, ..., f2, 1 ]; Y = [ Y1, ... Ym ]
# reasoning is equation = f1 * b1 + ... fm * bm + f0 * 1, where f0 = a
# 2D Array notation: FY[range of outer array, range of inner array]
F = numpy.hstack( ( FY[:,:-1], numpy.ones((n,1)) ) )
Y = FY[:,-1]

# B = [ a, b1, ... bm ]
B = numpy.linalg.lstsq(F, Y, rcond=None)[0]

q = int(raw_input())

'''
# incorrect:
for i in range(q):
    f = list(map(float, raw_input().rstrip().split(" ")))
    print B[0] + sum([ B[1:][i] * f[i] for i in range(m) ])
# yields:
122.894240301
160.678751919
150.255937446
135.439240982
'''

F = numpy.array([raw_input().rstrip().split(" ") for _ in range(q)], float)
# Y = f1 * b1 + ... fm * bm + 1 * b0, where b0 = a
Y = numpy.hstack( ( F, numpy.ones((q,1)) ) ).dot(B)

s = 2 # significance
for y in Y:
    print round(y, s)


'''
Testcase0:
2 7
0.18 0.89 109.85
1.0 0.26 155.72
0.92 0.11 137.66
0.07 0.37 76.17
0.85 0.16 139.75
0.99 0.41 162.6
0.87 0.47 151.77
4
0.49 0.18
0.57 0.83
0.56 0.64
0.76 0.18

Output0:
105.22
142.68
132.94
129.71
'''

