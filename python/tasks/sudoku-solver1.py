# my initial attempt failed to completely solve
# leaving patches of zeroes all over the place

def test(g):
    for r in range(9):
        for c in range(9):
            if g[r][c] == 0:
                n = range(1, 10)
                #print 'TEST1', n
                for i in range(9):
                    if c != i and g[r][i] != 0:
                        if g[r][i] in n: # horizontal test
                            #print 'H -', g[r][c]
                            n.remove(g[r][i])
                    if r != i and g[i][c] != 0:
                        if g[i][c] in n: # vertical test
                            #print 'V -', g[r][c]
                            n.remove(g[i][c])
                    x = i/3 + 3 * (r/3)
                    y = i%3 + 3 * (c/3)
                    #print 'Q', x, y
                    if r != x and r != y and g[x][y] != 0:
                        if g[x][y] in n: # quadrant test
                            #print 'Q -', g[x][y]
                            n.remove(g[x][y])
                #print 'TEST2', n
                yield(r, c, n)

def sudoku_solve(grid):
    import os
    os.system('clear')
    #print '====='
    print '\n'.join([' '.join([str(c) for c in r]) for r in grid])
    if sum([sum(r) for r in grid]) == 45 * 9:
        return true
    for s in test(grid):
        print 'SET', s
        r, c, N = s;
        if len(N) > 0:
            for n in N:
                print 'FILL', r, c, n
                grid[r][c] = n
                if sudoku_solve(grid):
                    return true
                grid[r][c] = 0
    return False
    
n = input()

for i in range(n):
    board = []
    for j in range(9):
        board.append([int(k) for k in raw_input().split()])
    sudoku_solve(board)
