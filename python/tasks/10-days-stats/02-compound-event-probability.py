# https://www.hackerrank.com/challenges/s10-mcq-3/problem

''' 
There are  urns labeled X, Y, and Z. 
* Urn X contains 4 red balls and 3 black balls.
* Urn Y contains 5 red balls and 4 black balls.
* Urn Z contains 4 red balls and 4 black balls. 
'''
# One ball is drawn from each of the 3 urns. What is the probability that, of the 3 balls drawn, 2 are red and 1 is black?

# http://www.fileformat.info/info/unicode/char/2229/index.htm
# Intersection, multiplication rule:
# P(A and B) = P(A) x P(B)

'''
Urn X:  P(Red) = 4/7    P(Black) = 3/7
Urn Y:  P(Red) = 5/9    P(Black) = 4/9
Urn Z:  P(Red) = 1/2    P(Black) = 1/2
'''

'''
  P(2 Red, 1 Black) = P(Red Red Black) + P(Red Black Red) + P(Black Red Red)
                    = (4/7)(5/9)(1/2) + (4/7)(4/9)(1/2) + (3/7)(5/9)(1/2)
                    = 20/126 + 16/126 + 15/126 
                    = 51/126 
                    = 17/42
'''
print 4*5 + 4*4 + 3*5
print 7 * 9 * 2

print (4*5 + 4*4 + 3*5) / 3
print (7 * 9 * 2) / 3

