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
screen = pygame.display.set_mode((400, 700))
fps = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Matching Numbers")
program_icon = pygame.image.load('img\icon.png')
pygame.display.set_icon(program_icon)

##################
## Window setup ##
##################
font = ['Arial', 20]

class Window:
    def __init__(self):
        self.objects = []
    
    def run(self):
        for object in self.objects:
            object.process(screen)

menu_window = Window()

def continue_game():
    print("Continue button pressed")
    global window
    window = "game"
Button(menu_window.objects, 150, 10, 100, 30, 'Continue', continue_game, True, font = font)

def go_2_settings():
    print("Settings button pressed")
    # global window
    # window = "settings"
Button(menu_window.objects, 150, 50, 100, 30, 'Settings', go_2_settings, True, font = font)

def exit():
    global run
    run = False
Button(menu_window.objects, 150, 90, 100, 30, 'Exit', exit, font = font)

game_window = Window()

def go_2_menu():
    print("Menu button pressed")
    global window
    window = "menu"
Button(game_window.objects, 10, 10, 100, 30, 'Menu', go_2_menu, font = font)

#################
## Window Loop ##
#################

run = True
window = "game"
while run:
    screen.fill((0, 0, 0)) # reset canvas

    # user imputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close the game
            run = False
    
    # switch windows
    if window == "game":
        game_window.run()
    elif window == "menu":
        menu_window.run()
    else: window = "menu"
    
    # update display window
    # pygame.display.flip() # pygame.display.update(), but only part of the screen
    pygame.display.update()

    # delay
    fpsClock.tick(fps)
pygame.quit()
sys.exit()