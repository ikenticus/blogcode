# Easy
# https://www.hackerrank.com/challenges/s10-spearman-rank-correlation-coefficient/problem

'''
Objective 

In this challenge, we practice calculating Spearman's rank correlation coefficient. Check out the Tutorial tab for learning materials!

Task

Given two n-element data sets, X and Y, calculate the value of Spearman's rank correlation coefficient.

Input Format

The first line contains an integer, n, denoting the number of values in data sets X and Y. 
The second line contains n space-separated real numbers (scaled to at most one decimal place) denoting data set X. 
The third line contains n space-separated real numbers (scaled to at most one decimal place) denoting data set Y.

Constraints

  10 <= n <= 100
  1 <= xi <= 500, where xi is the ith value of data set X.
  1 <= yi <= 500, where yi is the ith value of data set Y.
* Data set X contains unique values.
* Data set Y contains unique values.

Output Format

Print the value of the Spearman's rank correlation coefficient, rounded to a scale of 3 decimal places.

Sample Input

10
10 9.8 8 7.8 7.7 1.7 6 5 1.4 2 
200 44 32 24 22 17 15 12 8 4

Sample Output

0.903

Explanation

We know that data sets X and Y both contain unique values, so the rank of each value in each data set is unique. Because of this property, we can use the following formula to calculate the value of Spearman's rank correlation coefficient:

               6 Sum di^2
    r xy = 1 - ----------
               N(N^2 - 1)

Here, di is the difference between ranks of each pair (xi, yi). The following table shows the calculation of di^2:

     X    Y   rx  ry  di  di^2
    10   200  10  10   0   0
     9.8  44   9   9   0   0
     8    32   8   8   0   0
     7.8  24   7   7   0   0
     7.7  22   6   6   0   0
     1.7  17   2   5  -3   9
     6    15   5   4   1   1
     5    12   4   3   1   1
     1.4   8   1   2  -1   1
     2     4   3   1   2   4

Now, we find the value of the coefficient:

            6 * 16
    r = 1 - ------- = 1 - 0.09696969696 = 0.903030303
            10 * 99

When rounded to a scale of three decimal places, we get 0.903 as our final answer.
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
s = 3   # significance

# spearman rank correlation coefficient
def spearman(N, D):
    return 1 - 6.0 * sum(D) / N / (N**2 - 1)

N = int(raw_input())
X = list(map(float, raw_input().rstrip().split(" ")))
Y = list(map(float, raw_input().rstrip().split(" ")))

Xr = X[:]
Xr.sort(reverse=True)
Yr = Y[:]
Yr.sort(reverse=True)

#D = [ Xr.index(X[i]) - Yr.index(Y[i]) for i in range(N) ]
D2 = [ (Xr.index(X[i]) - Yr.index(Y[i]))**2 for i in range(N) ]

print round(spearman(N, D2), s)

