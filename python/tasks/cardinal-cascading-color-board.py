# Implement the function update_board(board, color) for the following game.

# Given a m x n grid (3x3, or 10x20 for example),
# initialized so that each tile is assigned a color from a 4-color palette (RGBY).
# The user chooses one of those four colors.
# The upper left hand corner of the board is updated to the new color,
# as well as any tile that was "connected" to the upper left tile before the update.
# Connecting points are defined as any square you can get to by taking NSWE steps without going over a different color (no diagonals).

# For example, the board

# R R B
# G B R
# G B R

# With input B becomes:

# B B B
# G B R
# G B R

# With input G becomes:

# G G G
# G G R
# G G R

# def update_board(board, color):
#     pass

def find_neighbors_of_same_color(board, square=[0,0]):
    neighbors = []
    max = [len(board) - 1, len(board[0]) - 1]
    y,x = square

    if y > 0 and board[y-1][x] == board[y][x]:
        neighbors.append([y-1, x])
    if y < max[0] and board[y+1][x] == board[y][x]:
        neighbors.append([y+1, x])
    if x > 0 and board[y][x-1] == board[y][x]:
        neighbors.append([y, x-1])
    if x < max[1] and board[y][x+1] == board[y][x]:
        neighbors.append([y, x+1])

    # return the list of NSWE direct neighbors that are the same color as input square
    return neighbors

def find_all_connected_square_coordinates(board):
    color = board[0][0]
    connected = find_neighbors_of_same_color(board, [0,0])
    my = len(board)
    mx = len(board[0])
    for by in range(0, my):
        for bx in range(0, mx):
            if [by,bx] in connected and board[by][bx] == color:
                for c in find_neighbors_of_same_color(board, [by,bx]):
                    if c not in connected:
                        connected.append(c)
    return connected

def update_board(board, color):
    for box in find_all_connected_square_coordinates(board):
        board[box[0]][box[1]] = color
    return board

B0 = [
    ['R','R','B'],
    ['G','B','R'],
    ['G','B','R'],
]

B1 = update_board(B0, 'B')
for y in B1:
    print(y)

print()

B2 = update_board(B1, 'G')
for y in B2:
    print(y)
