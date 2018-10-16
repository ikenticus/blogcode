
lines = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

def winner(grid):
    for line in lines:
        [a, b, c] = line
        if grid[a] != ' ' and grid[a] == grid[b] and grid[a] == grid[c]:
            return grid[a]
    return False

def game_over(grid):
    who = winner(grid)
    if who:
        print '%s Wins' % who
        return True
        
    if ' ' not in grid:
        print 'Game Tied'
        return True
    else:
        return False

def next_move(grid, turn):
    print 'Enter box (1-9):',
    entry = int(raw_input()) - 1
    if grid[entry] == ' ':
        grid[entry] = turn
    else:
        next_move(grid, turn)
    show_nice(grid)
    return grid

def show_nice(grid):
    for r in xrange(3):
        print '\n\t',
        for c in xrange(3):
            lead = ' ' if c == 0 else ''
            line = ' |' if c < 2 else ''
            print '%s%s%s' % (lead, grid[c+r*3], line),
        if r < 2:
            print '\n\t---+---+---',
    print '\n'
            
if __name__ == "__main__":
    turn = 'X'
    grid = [ ' ' for _ in xrange(9) ]
    while not game_over(grid):
        grid = next_move(grid, turn)
        turn = 'O' if turn == 'X' else 'X'

