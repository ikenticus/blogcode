# Easy
# https://www.hackerrank.com/challenges/s10-pearson-correlation-coefficient/problem

'''
Objective 

In this challenge, we practice calculating the Pearson correlation coefficient. Check out the Tutorial tab for learning materials!

Task

Given two n-element data sets, X and Y, calculate the value of the Pearson correlation coefficient.

Input Format

The first line contains an integer, n, denoting the size of data sets X and Y. 
The second line contains n space-separated real numbers (scaled to at most one decimal place), defining data set X. 
The third line contains n space-separated real numbers (scaled to at most one decimal place), defining data set Y.

Constraints

  10 <= n <= 100
  1 < xi <= 500, where xi is the ith value of data set X.
  1 < yi <= 500, where yi is the ith value of data set Y.
* Data set X contains unique values.
* Data set Y contains unique values.

Output Format

Print the value of the Pearson correlation coefficient, rounded to a scale of 3 decimal places.

Sample Input

10
10 9.8 8 7.8 7.7 7 6 5 4 2 
200 44 32 24 22 17 15 12 8 4

Sample Output

0.612

Explanation

The mean and standard deviation of data set X are:
* mux = 6.73
* sdx = 2.39251

The mean and standard deviation of data set Y are:
* mux = 37.8
* sdx = 55.1993

We use the following formula to calculate the Pearson correlation coefficient:

             Sum (xi - mux) * (yi - muy)
    P(X,Y) = ---------------------------
                    n * sdx * sdy       

'''

# Enter your code here. Read input from STDIN. Print output to STDOUT

# pearson correlation coefficient
def P(n, S, mu, sd):
    return sum([ (S['x'][i] - mu['x']) * (S['y'][i] - mu['y']) for i in range(n) ]) / (n * sd['x'] * sd['y'])

# calculate mean:
def mean(S):
    return sum(S) / len(S)

# calculate standard deviation:
def stdev(S, mu):
    return (sum([ (i - mu) ** 2 for i in S ]) / len(S)) ** 0.5

s = 3   # significance
n = int(raw_input())

S = {}
S['x'] = list(map(float, raw_input().rstrip().split(" ")))
S['y'] = list(map(float, raw_input().rstrip().split(" ")))

mu = {}
mu['x'] = mean(S['x'])
mu['y'] = mean(S['y'])

sd = {}
sd['x'] = stdev(S['x'], mu['x'])
sd['y'] = stdev(S['y'], mu['y'])

print round(P(n, S, mu, sd), s)

'''
Testcase0: 0.612
10
10 9.8 8 7.8 7.7 7 6 5 4 2 
200 44 32 24 22 17 15 12 8 4

# stupidly used the given mu/sd values for case0 in case1
Testcase1: 0.299
10
10 9.8 8 7.8 7.7 7 6 15 4 2 
200 414 32 24 212 17 15 12 8 4
'''

'''
# python2 similar:
def m(x):
    return sum(x) / n

def sd(x):
    mx = m(x)
    return ((sum([(i - mx)**2 for i in x])) / n)**0.5

def cov(x, y): # covariance
    mx, my, sx, sy = m(x), m(y), sd(x), sd(y)
    return sum([(i - mx)*(j - my) for i, j in zip(x, y)]) / (n * sx * sy)

n = int(input())
x = [float(i) for i in input().split()]
y = [float(j) for j in input().split()]

print(round(cov(x, y), 3))

# python3 optimized:
devX = list(map(lambda x: x - sum(X) / N, X))
devY = list(map(lambda x: x - sum(Y) / N, Y))
sdevX = (sum(map(lambda x: x**2, devX)) / N)**0.5
sdevY = (sum(map(lambda x: x**2, devY)) / N)**0.5
covXY = sum(list(map(lambda x,y: x*y,devX, devY)))
print(round(covXY / (N * sdevX * sdevY),3))
'''
