# Easy
# https://www.hackerrank.com/challenges/s10-the-central-limit-theorem-2/problem

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

In this challenge, we practice solving problems based on the Central Limit Theorem. We recommend reviewing the Central Limit Theorem Tutorial before attempting this challenge.

Task 

The number of tickets purchased by each student for the University X vs. University Y football game follows a distribution that has a mean of mu = 2.4 and a standard deviation of sd = 2.0.

A few hours before the game starts, 100 eager students line up to purchase last-minute tickets. If there are only 250 tickets left, what is the probability that all 100 students will be able to purchase tickets?

Input Format

There are 4 lines of input (shown below):

250
100
2.4
2.0

The first line contains the number of last-minute tickets available at the box office. The second line contains the number of students waiting to buy tickets. The third line contains the mean number of purchased tickets, and the fourth line contains the standard deviation.

If you do not wish to read this information from stdin, you can hard-code it into your program.

Output Format

Print the probability that 100 students can successfully purchase the remaining 250 tickets, rounded to a scale of 4 decimal places (i.e., 1.2345 format).
'''

# Enter your code here. Read input from STDIN. Print output to STDOUT
import math

# cumulative distribution function
def Phi(x, mu, sd):
    return (1 + math.erf((x - mu) / sd / math.sqrt(2))) / 2

x = int(raw_input())
n = int(raw_input())
mu = float(raw_input())
sd = float(raw_input())

s = 4   # significance

# per tutorial, for large n, the Sample sum is close to N(mu1,sd1) where
mu1 = n * mu
sd1 = math.sqrt(n) * sd

print round(Phi(x, mu1, sd1), s)

