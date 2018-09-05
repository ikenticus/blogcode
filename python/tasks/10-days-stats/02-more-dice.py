# https://www.hackerrank.com/challenges/s10-mcq-2/problem

# In a single toss of 2 fair (evenly-weighted) six-sided dice, find the probability that the values rolled by each die will be different and the two dice have a sum of 6.

# P(A) = Number of favorable outcomes / Total number of outcomes

# Total number of outcomes for 2 fair dice: 36
print 6 * 6

# Total sum outcomes, asterisk for i != j, sum = 9:
for i in range(1, 7):
    for j in range(1, 7):
        mark = '*' if (i != j and i+j == 6) else ' '
        print '%02d%s ' % (i+j, mark),
    print

# P(A) = 4 / 36 => 1 / 9


