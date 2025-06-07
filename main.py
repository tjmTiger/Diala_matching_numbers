from number import *
from board import *
import random

board = []

for i in range(1,36):
    board.append(Number(random.randint(1,9)))

board = Board(board)
print(board)
print(board[1][1])