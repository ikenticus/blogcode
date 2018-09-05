# https://www.hackerrank.com/challenges/s10-mcq-1/problem

# In a single toss of 2 fair (evenly-weighted) six-sided dice, find the probability that their sum will be at most 9.

# P(A) = Number of favorable outcomes / Total number of outcomes

# Total number of outcomes for 2 fair dice: 36
print 6 * 6

# Total sum outcomes, asterisk for <= 9:
for i in range(1, 7):
    for j in range(1, 7):
        mark = '*' if (i+j <= 9) else ' '
        print '%02d%s ' % (i+j, mark),
    print

# P(A) = 30 / 36 => 5 / 6


