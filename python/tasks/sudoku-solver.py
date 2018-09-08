#!/bin/python

def sudoku_solve(grid):
    "your logic here"


n = input()

for i in range(n):
    board = []
    for j in range(9):
        board.append([int(k) for k in raw_input().split()])
    sudoku_solve(board)
