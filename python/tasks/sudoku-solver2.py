import random
F = range(9)
random.shuffle(F)

def free(g):
    for r in F:
        for c in F:
            if g[r][c] == 0:
                #print 'FREE', r, c
                return [r, c]   
    return False

def box(g, r, c, n):
    for x in range(3):
        for y in range(3):
            if g[r+x][c+y] == n:
                return True
    return False

def col(g, c, n):
    for i in range(9):
        if g[i][c] == n:
            return True
    return False

def row(g, r, n):
    for i in range(9):
        if g[r][i] == n:
            return True
    return False

def safe(g, r, c, n):
    return not row(g, r, n) and not col(g, c, n) and not box(g, r - r%3, c - c%3, n)

def sudoku_solve(g):
    import os
    os.system('clear')
    print '\n'.join([' '.join([str(c) for c in r]) for r in g])

    p = free(g) # pointer to grid location, starting from upper left
    if not p:   # if no more free spaces, done
        return True

    #print 'TEST', p
    r, c = p
    for n in range(1, 10):
        #print 'TRY', n
        if safe(g, r, c, n):
            #print r, c, 'SAFE', n
            g[r][c] = n
            if sudoku_solve(g): # solved?
                return True
            g[r][c] = 0         # revert
    return False

'''
Solved:
1
3 0 6 5 0 8 4 0 0
5 2 0 0 0 0 0 0 0
0 8 7 0 0 0 0 3 1
0 0 3 0 1 0 0 8 0
9 0 0 8 6 3 0 0 5
0 5 0 0 9 0 6 0 0
1 3 0 0 0 0 2 5 0
0 0 0 0 0 0 0 7 4
0 0 5 2 0 6 3 0 0

3 1 6 5 7 8 4 9 2
5 2 9 1 3 4 7 6 8
4 8 7 6 2 9 5 3 1
2 6 3 4 1 5 9 8 7
9 7 4 8 6 3 1 2 5
8 5 1 7 9 2 6 4 3
1 3 8 9 4 7 2 5 6
6 9 2 3 5 1 8 7 4
7 4 5 2 8 6 3 1 9

real	0m8.753s
user	0m1.973s
sys	0m1.786s

And this one:
1
0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0

1 2 3 4 5 7 6 8 9
5 6 8 1 2 9 3 4 7
4 7 9 3 6 8 1 2 5
3 1 2 5 4 6 7 9 8
6 4 7 8 9 1 5 3 2
8 9 5 2 7 3 4 1 6
2 3 1 6 8 5 9 7 4
7 8 6 9 1 4 2 5 3
9 5 4 7 3 2 8 6 1

real	0m2.855s
user	0m0.502s
sys	0m0.454s

But not the Testcase from HackRank:
1
4 0 0 0 0 6 0 0 0
0 6 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 6 0 0 2 0
1 0 0 0 0 0 9 0 0
8 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 5

Discussions had this output:
4 1 5 2 9 6 3 7 8
2 6 7 1 3 8 4 5 9
3 9 8 4 5 7 1 6 2
5 4 2 3 7 1 8 9 6
6 7 1 8 2 9 5 3 4
9 8 3 5 6 4 7 2 1
1 5 6 7 4 2 9 8 3
8 3 9 6 1 5 2 4 7
7 2 4 9 8 3 6 1 5

After adding a random shuffle:
4 9 8 2 3 6 5 1 7
7 6 5 4 1 8 2 3 9
3 2 1 7 5 9 4 6 8
6 7 2 5 4 3 8 9 1
9 1 4 8 2 7 3 5 6
5 8 3 9 6 1 7 2 4
1 5 7 6 8 2 9 4 3
8 4 6 3 9 5 1 7 2
2 3 9 1 7 4 6 8 5

real	0m35.268s
user	0m16.411s
sys	0m14.866s
'''
    
n = input()

for i in range(n):
    board = []
    for j in range(9):
        board.append([int(k) for k in raw_input().split()])
    sudoku_solve(board)
