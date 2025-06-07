# local
from board import *
from gui import *

# standard library
import random

# external
import pygame # om du får error om att du saknar pygame, i terminalen skriv "pip install pygame" och tryck enter

board = Board() # int_list = list(range(1,9)))
print(board)
print("-"*9)
board[0][1].gray = True
board.add()
print(board)

########################
## Pygame Innitiation ##
########################

pygame.init()
screen = pygame.display.set_mode((400, 600))
fps = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Matching Numbers")
program_icon = pygame.image.load('img\icon.png')
pygame.display.set_icon(program_icon)

#################
## Window Loop ##
#################

run = True
while run:
    # user imputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close the game
            run = False

    
    # update display window
    pygame.display.update()

    # delay
    fpsClock.tick(fps)
pygame.quit()