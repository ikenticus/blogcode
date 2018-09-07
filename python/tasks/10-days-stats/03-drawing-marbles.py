# https://www.hackerrank.com/challenges/s10-mcq-6/problem

# A bag contains 3 red marbles and 4 blue marbles. Then, 2 marbles are drawn from the bag, at random, without replacement. If the first marble drawn is red, what is the probability that the second marble is blue?

'''
7 marbles
1st red: 3 / 7
2nd blue: 4 / 6

If the question was the possibility of drawing a red followed by a blue, then:

    P(R|B) = 3 / 7 * 4 / 6 = 2 / 7 ?

However, since it only ask what the possibility of a blue after the first being red was already known,
the two case are independent of each other and the P(B) = 4 / 6 = 2 / 3

'''
