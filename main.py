from number import *  # noqa: F403
from board import *  # noqa: F403
import pygame

board = Board() # int_list = list(range(1,9)))  # noqa: F405
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
pygame.display.set_caption("Matching Numbers")
# program_icon = pygame.image.load('img\icon.png')
# pygame.display.set_icon(program_icon)

#################
## Window Loop ##
#################

run = True
while run:
    #User imputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close the game
            run = False

    
    #update display window
    pygame.display.update()
pygame.quit()