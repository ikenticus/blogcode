#!/bin/python

import math
import os
import random
import re
import sys

def check(crossword, word):
    slots = []
    length = len(word)
    for row in range(10):
        for col in range(10):
            validH = True
            validV = True
            for w in range(length):
                if col <= 10 - length:
                    if crossword[row][col + w] not in  ['-', word[w]]:
                        validH = False
                if row <= 10 - length:
                    if crossword[row + w][col] not in  ['-', word[w]]:
                        validV = False
            if validH and col <= 10 - length:
                yield(row, col, 'H')
            if validV and row <= 10 - length:
                yield(row, col, 'V')

def writePuzzle(crossword, word, slot, empty = False):
    row, col, dir = slot;
    for w in range(len(word)):
        letter = empty if empty else word[w]
        if dir == 'H':
            crossword[row][col + w] = letter
        else:
            crossword[row + w][col] = letter

# recombine split crossword_item row lists back into row strings
def merge(crossword):
    board = []
    if isinstance(crossword[0], list):
        for row in crossword:
            board.append(''.join(row))
    else:
        board = crossword
    return board

# Complete the crosswordPuzzle function below.
def crosswordPuzzle(crossword, words):
    if len(words) == 0:
        return crossword
    word = words.pop()
    for slot in check(crossword, word):
        writePuzzle(crossword, word, slot)
        board = crosswordPuzzle(crossword, words)
        if board:
            return merge(board)
        else:
            writePuzzle(crossword, word, slot, '-');
    words.append(word)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    crossword = []

    for _ in xrange(10):
        crossword_item = list(raw_input())
        # split items into letter list instead of string
        crossword.append(crossword_item)

    # split semi-colon into list
    words = raw_input().split(';')

    result = crosswordPuzzle(crossword, words)
    print result
    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()

