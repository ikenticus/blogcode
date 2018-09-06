# https://www.hackerrank.com/challenges/s10-mcq-4/problem

# Conditional Probability
'''
This is defined as the probability of an event occurring, assuming that one or more other events have already occurred. Two events, A and B are considered to be independent if event A has no effect on the probability of event B (i.e. P(B|A) = P(B)). If events A and B are not independent, then we must consider the probability that both events occur. This can be referred to as the intersection of events A and B, defined as P(A∩B) = P(B|A) * P(A). We can then use this definition to find the conditional probability by dividing the probability of the intersection of the two events (A∩B) by the probability of the event that is assumed to have already occurred (event A):

           P(A∩B)
  P(B|A) = ------
            P(A)
'''

# Bayes' Theorem
'''
Let A and B be two events such that P(A|B) denotes the probability of the occurrence of A given that B has occurred and P(B|A) denotes the probability of the occurrence of B given that A has occurred, then:

           P(B|A) * P(A)             P(B|A) * P(A)          
  P(A|B) = ------------- = ---------------------------------
               P(B)        P(B|A) * P(A) + P(B|A^c) * P(A^c) 
'''

# Suppose a family has 2 children, one of which is a boy. What is the probability that both children are boys?

'''
    B   G
  B BB  BG
  G GB  GG
'''
# Conditional: P(B|A) = P(2Boys|1Boy) = P(BothBoys)/P(1Boy) = 1/4 / 3/4 = 1/3

# Phrased like the first part of https://imgur.com/a/sr8lw instead of the second:

# Suppose instead we are told that one child is a boy.  What is the probability that the other child is a boy:

# Bayesian: P(Boy2|Boy1) = 1/2 * 1/4 / 1/4 = 1/2 ?
 



