# local
from board import *
from gui import *

# standard library
import sys

# external
import pygame # om du får error om att du saknar pygame, i terminalen skriv "pip install pygame" och tryck enter

board = Board() # [1]*35
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


menu_window = Window(screen)

def continue_game():
    global window
    window = "game"
Button(menu_window.objects, 150, 10, 100, 30, 'Continue', continue_game, True, font = font)

def go_2_settings():
    global window
    window = "settings"
Button(menu_window.objects, 150, 50, 100, 30, 'Settings', go_2_settings, True, font = font)

def exit():
    global run
    run = False
Button(menu_window.objects, 150, 90, 100, 30, 'Exit', exit, font = font)

##################
game_window = Window(screen)

def go_2_menu():
    print("Menu button pressed")
    global window
    window = "menu"
Button(game_window.objects, 20, 10, 100, 30, 'Menu', go_2_menu, font = font)

# todo: finish + button and score count with display
def print_click():
    print("click")
Button(game_window.objects, 150, 50, 100, 30, 'Score:', print_click, font = font)
Button(game_window.objects, 350, 50, 30, 30, '+', print_click, font = font)

game_board = ButtonGroup(game_window.objects)

def adjucent(button1, button2):
    gray_buttons = []
    global game_board
    for b in range(len(game_board.objects)):
        if game_board.objects[b].number.gray:
            gray_buttons.append(b)
            
    b1 = game_board.objects.index(button1)
    b2 = game_board.objects.index(button2)
    print(gray_buttons)

    # horisontal left & vertical up
    for i in [1,9]:
        b = b1-i
        while b >=0 and b in gray_buttons:
            b -= i
        else:
            if b == b2:
                return True
    # horisontal right & vertical down
    for i in [1,9]:
        b = b1+i
        while b <= len(game_board.objects) and b in gray_buttons:
            b += i
        else:
            if b == b2:
                return True
    # special case horisontal right (looping)
    if (b+1)%9 == 0 and b != 8:
        b = b1 - 17
        while b < b1 and b in gray_buttons:
            b += 1
        else:
            if b == b2:
                return True
    # diagonal
    for i in [-10, -8, 8, 10]:
        b = b1+i
        while b >= 0 and b <= len(game_board.objects) and b in gray_buttons:
            b+=i
        else:
            if b == b2 and not ((b+1)%9 == 0 and i in [-10, 8]):
                return True
    return False

selected = []
def clicked_number(button):
    global selected
    if not button.number.gray:
        if len(selected) == 1:
            if (selected[0] != button) and adjucent(selected[0], button):
                selected.append(button)
        else:
            selected = [button]

    if len(selected) == 1:
        print("[{}, ]".format(selected[0].number))
    elif len(selected) == 2:
        print("[{}]".format(str(selected[0].number) + ", " + str(selected[1].number)))
        if selected[0].number == selected[1].number or selected[0].number + selected[1].number == 10:
            selected[0].number.gray = True
            selected[1].number.gray = True
    else:
        print(selected)

for y in range(len(board)):
    for x in range(len(board[y])):
        NumberButton(game_board.objects, 40*x+20, 40*y+100, 40, 40, board[y][x], clicked_number, font = font)


#################
## Window Loop ##
#################

run = True
window = "game"
while run:
    screen.fill((250, 218, 221)) # reset canvas

    # user imputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close the game
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: # right mouse button
                selected = []
                print("[]")
    
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