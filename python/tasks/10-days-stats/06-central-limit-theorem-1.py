# Easy
# https://www.hackerrank.com/challenges/s10-the-central-limit-theorem-1/problem

# Central Limit Theorem
'''
The central limit theorem (CLT) states that, for a large enough sample n(), the distribution of the sample mean will approach normal distribution. This holds for a sample of independent random variables from any distribution with a finite standard deviation. 


Let {X1, X2, X3, ..., Xn} be a random data set of size n, that is, a sequence of independent and identically distributed random variables drawn from distributions of expected values given by mu and finite variances given by sd^2. The sample average is:

          Sumi Xi
    sn := -------
             N   

For large n, the distribution of sample sums Sn is close to normal distribution N(mu',sd') where: 

    mu' = n * mu
    sd' = sqrt(n) * sd

'''


'''
Objective 

In this challenge, we practice solving problems based on the Central Limit Theorem. Check out the Tutorial tab for learning materials!

Task 

A large elevator can transport a maximum of 9800 pounds. Suppose a load of cargo containing 49 boxes must be transported via the elevator. The box weight of this type of cargo follows a distribution with a mean of mu = 205 pounds and a standard deviation of sd = 15 pounds. Based on this information, what is the probability that all 49 boxes can be safely loaded into the freight elevator and transported?

Input Format

There are 4 lines of input (shown below):

9800
49
205
15

The first line contains the maximum weight the elevator can transport. The second line contains the number of boxes in the cargo. The third line contains the mean weight of a cargo box, and the fourth line contains its standard deviation.

If you do not wish to read this information from stdin, you can hard-code it into your program.

Output Format

Print the probability that the elevator can successfully transport all 49 boxes, rounded to a scale of 4 decimal places (i.e., 1.2345 format).
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
import math

# cumulative distribution function
def Phi(x, mu, sd):
    return (1 + math.erf((x - mu) / sd / math.sqrt(2))) / 2

x = int(raw_input())
n = int(raw_input())
mu = int(raw_input())
sd = int(raw_input())

s = 4   # significance

# per tutorial, for large n, the Sample sum is close to N(mu1,sd1) where
mu1 = n * mu
sd1 = math.sqrt(n) * sd

print round(Phi(x, mu1, sd1), s)

