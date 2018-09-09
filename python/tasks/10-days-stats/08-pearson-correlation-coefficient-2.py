# https://www.hackerrank.com/challenges/s10-mcq-7/problem

'''
Regression Line

If our data shows a linear relationship between X and Y, then the straight line which best describes the relationship is the regression line. The regression line is given by ^Y = a + bX. 


Finding the Value of b

The value of b can be calculated using either of the following formulae:

        n * sum(xi, yi) - sum(xi) * sum(yi)
    b = -----------------------------------
             n * sum(xi^2) - sum(xi)^2     

            sd y
    b = p * ---- , where p is the Pearson correlation coefficient,
            sd x
        
sd x is the standard deviation of X and sd y is the standard deviation of Y. 

Finding the Value of a

    a = mu y - b * mu x, where mu x is the mean of X and mu y is the mean of Y. 

'''

'''
The regression line of y on x is 3x + 4y + 8 = 0,
and the regression line of x on y is 4x + 3y + 7 = 0.
What is the value of the Pearson correlation coefficient?

    1               -1
    3 / 4           -4 / 3
    4 / 3           -3 / 4

'''

# rewrite the formulas
'''
    3x + 4y + 8 = 0
    y = (-8 - 3x)/4 = -2 + (-3/4)x

    4x + 3y + 7 = 0
    x = (-7 -3y)/4 = -7/4 + (-3/4)y

    Both written as Regression Line: ^Y = a + bX
    Making bx = by = -3/4
'''

# rewrite the regression line b formula
'''
    bx = p * sd x / sd y
    by = p * sd y / sd x
    bx * by = p^2
    p = 3/4 or -3/4

    since both regression lines have negative slopes, the answer will be negative
'''
