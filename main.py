# local
from board import *
from gui import *

# standard library
import sys
import os

# external
import pygame # om du får error om att du saknar pygame, i terminalen skriv "pip install pygame" och tryck enter

########################
## Pygame Innitiation ##
########################

pygame.init()
screen = pygame.display.set_mode((400, 700))
fps = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Matching Numbers")
path = os.getcwd()
program_icon = pygame.image.load(path + '/img/icon.png')
pygame.display.set_icon(program_icon)

board = Board([1]*35) # [1]*35
print(board)

##################
## Window setup ##
##################
font = ['Arial', 20]

##     Game     ##
game_window = Window()

def go_2_menu():
    global window
    window = "menu"
Button(game_window.objects, 20, 10, 100, 30, 'Menu', go_2_menu, font = font)

Button(game_window.objects, 350, 50, 30, 30, '+', board.add, font = font)

# todo: finish + button and score count with display
DisplayButton(game_window.objects, 150, 50, 100, 30, 'Score: ', font = font)

game_board = ButtonGroup(game_window.objects)

selected = []
def clicked_number(button):
    global selected
    if len(selected) == 1 and not button.number.gray: # if only one button selected, add secound, otherwise reset selection
        if (selected[0] != button) and game_board.adjacent(selected[0], button):
            selected.append(button)
        else: # if invalid move, reset selection
            selected = []
    elif not button.number.gray: # reset selection
        selected = [button]

    if len(selected) == 2: # if two selected and they r a valid pair, make them gray
        if selected[0].number == selected[1].number or selected[0].number + selected[1].number == 10:
            selected[0].number.gray = True
            selected[1].number.gray = True
            board.score += 2
            selected = []

for y in range(len(board)):
    for x in range(len(board[y])):
        NumberButton(game_board.objects, 40*x+20, 40*y+100, 40, 40, board[y][x], clicked_number, font = font)

##     Menu     ##
menu_window = Window()

def continue_game():
    global window
    window = "game"
Button(menu_window.objects, 150, 10, 100, 30, 'Continue', continue_game, True, font = font)

def new_game():
    global board
    global window
    global selected
    board.new_game(random.choices(range(1,10), k=35))
    game_board.clear_objects()
    selected = []
    window = "game"
    print(board)
Button(menu_window.objects, 150, 50, 100, 30, 'New Game', new_game, True, font = font)

def exit():
    global run
    run = False
Button(menu_window.objects, 150, 90, 100, 30, 'Exit', exit, font = font)

#################
## Window Loop ##
#################
def update_board():
    global board
    global game_board
    # remove old buttons
    if board.remove_gray_rows():
        game_board.clear_objects()
        # add new buttons
        for y in range(len(board)):
            for x in range(len(board[y])):
                NumberButton(game_board.objects, 40*x+20, 40*y+100, 40, 40, board[y][x], clicked_number, font = font)
    else:
        # add new buttons
        skip_existing = len(game_board.objects)
        for y in range(len(board)):
            for x in range(len(board[y])):
                if skip_existing <= 0:
                    NumberButton(game_board.objects, 40*x+20, 40*y+100, 40, 40, board[y][x], clicked_number, font = font)
                else: skip_existing -= 1

run = True
window = "game"
while run:
    update_board()
    screen.fill((250, 218, 221)) # reset canvas

    # user imputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close the game
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: # right mouse button
                selected = []
    
    # switch windows
    if window == "game":
        game_window.run([screen, board.score])
    elif window == "menu":
        menu_window.run([screen, board.score])
    else: window = "game"
    
    # update display window
    pygame.display.flip() # pygame.display.update(), but only part of the screen
    # pygame.display.update()

    # delay
    fpsClock.tick(fps)
pygame.quit()
sys.exit()