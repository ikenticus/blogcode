# https://www.hackerrank.com/challenges/s10-mcq-5/problem

# Permutations
'''
An ordered arrangement of r objects from a set, A, of n objects (where 0 < r <= n) is called an r-element permutation of A. You can also think of this as a permutation of A's elements taken r at a time. The number of r-element permutations of an n-object set is denoted by the following formula:

             n!   
    nPr = --------
          (n - r)!

                                                    n!
Note: We define 0! to be 1; otherwise, nPn would be -- (when r = n). 
                                                    0

'''

# Combinations
'''
An unordered arrangement of r objects from a set, A, of n objects (where r <= n) is called an r-element combination of A. You can also think of this as a combination of A's elements taken r at a time. 

Because the only difference between permutations and combinations is that combinations are unordered, we can easily find the number of r-element combinations by dividing out the permutations (r!):

          nPr         n!   
    nCr = --- = -------------
           r!   r! * (n - r)!

When we talk about combinations, we're talking about the number of subsets of size r that can be made from a set of size n. In fact, nCr is often referred to as "n choose r", because it's counting the number of r-element combinations that can be chosen from a set of n elements. In notation, nCr is typically written as:

    ( n )
    ( r )

'''

# You draw 2 cards from a standard 52-card deck without replacing them. What is the probability that both cards are of the same suit?

'''
52 cards, 13 * 4 suits
1st card: 13 / 52
2nd card: 12 / 51
Possibility with 1 suit = 13 / 52 * 12 / 51 = 3 / 51
Possibility with 4 suits = 4 * 3 / 51 = 12 / 51 = 4 / 17

                                                    13!        2! (52 - 2)!   4 * 13 * 12   4 * 13 * 3 * 4     4
Combination answer: 4 * C[13,2] / C[52,2] = 4 * ------------ * ------------ = ----------- = --------------- = --
                                                2! (13 - 2)!       52!          52 * 51     4 * 13 * 3 * 17   17
'''

# Simulation using python

import random

# the pair (x,y) refer to the value and suit of the card
cards = [(x,y) for x in range(13) for y in range(4)]
same, total = 0, 100000

for ii in range(total):
    s = random.sample(cards,2) # sample without replacement
    card_1_suit = s[0][1]
    card_2_suit = s[1][1]

    if card_1_suit == card_2_suit:
        same += 1

print(str(float(same) / total))
print(float(4)/17)
