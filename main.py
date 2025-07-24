# local
from board import *
from gui import *

# standard library
import sys
import os

# external
import pygame

########################
## Pygame Innitiation ##
########################

pygame.init()
screen = pygame.display.set_mode((400, 700))
fps = 60 # target fps
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Matching Numbers")
path = os.getcwd()
program_icon = pygame.image.load(path + '/img/icon.png')
pygame.display.set_icon(program_icon)

board = Board() # [1]*35;

###############
## GUI setup ##
###############
font = ['Arial', 20]

##     Game     ##
game_window = Window()

def go_2_menu():
    global window
    window = "menu"
Button(game_window.objects, 20, 10, 100, 30, 'Menu', go_2_menu, font = font)

add_button = Button(game_window.objects, 350, 50, 30, 30, '+', board.add, font = font)

def print_hint():
    print("Legal moves:")
    print(board.get_all_legal_moves())
    
# Button(game_window.objects, 300, 10, 80, 30, 'Hint', print_hint, font = font)

def show_add_count():
    return str(board.add_count)
DisplayButton(game_window.objects, 370, 70, 20, 20, '', show_add_count, font = font)

def show_score():
    return str(board.score)
DisplayButton(game_window.objects, 150, 50, 100, 30, 'Score: ',show_score , font = font)

board_buttons = ButtonGroup(game_window.objects)

selected = []
selection_button = DisplayButton(game_window.objects, -100, -100, 20, 3, "", color = "#E75480")
def clicked_number(button):
    global selected
    global selection_button
    if len(selected) == 1 and not button.number.gray: # if only one button selected, add secound, otherwise reset selection
        if (selected[0] != button) and board_buttons.adjacent(board, selected[0], button):
            selected.append(button)
        else: # if invalid move, reset selection
            selected = []
    elif not button.number.gray: # reset selection
        selected = [button]

    if len(selected) == 2: # if two selected and they r a valid pair, make them gray
        if selected[0].number == selected[1].number or selected[0].number + selected[1].number == 10:
            selected[0].number.gray = True
            selected[1].number.gray = True
            board.score += 1
            selected = []
    
    # highlight selected tile
    if selected:
        button = selected[0]
        selection_button.x = button.x+10
        selection_button.y = button.y+28
    else:
        selection_button.x = -100
        selection_button.y = -100
        

for y in range(len(board)):
    for x in range(len(board[y])):
        NumberButton(board_buttons.objects, 40*x+20, 40*y+100, 40, 40, board[y][x], clicked_number, font = font)

def update_board():
    global board
    global board_buttons
    # remove old buttons
    if board.remove_gray_rows():
        board_buttons.clear_objects()
        # add new buttons
        for y in range(len(board)):
            for x in range(len(board[y])):
                NumberButton(board_buttons.objects, 40*x+20, 40*y+100, 40, 40, board[y][x], clicked_number, font = font)
    else:
        # add new buttons
        skip_existing = len(board_buttons.objects)
        for y in range(len(board)):
            for x in range(len(board[y])):
                if skip_existing <= 0:
                    NumberButton(board_buttons.objects, 40*x+20, 40*y+100, 40, 40, board[y][x], clicked_number, font = font)
                else: skip_existing -= 1
    #todo: check if game over due to lack of moves (use board.get_legal_moves())
    if board.add_count == 0:
        no_moves = True
        for index in range(len(board.content_flat())):
            if board.get_legal_moves(index):
                no_moves = False
        if no_moves:
            print(no_moves)
            board.game_over = True

solution = []
solution_tiles = [DisplayButton(game_window.objects, -100, -100, 20, 3, "", color = "#2a929c"), 
                  DisplayButton(game_window.objects, -100, -100, 20, 3, "", color = "#2a929c")]
global solve_button
def get_solution():
    global solution
    global solution_next
    global solve_button
    solve_button.y = -100
    solution = board.find_solution()
    print("Solution")
    print(solution)
    
    def solution_next_func():
        global solution
        global solution_tiles
        if solution["moves"]:
            move = solution["moves"].pop(0)
            if move[0] == "+":
                for i in range(2):
                    solution_tiles[i].x = add_button.x + 10
                    solution_tiles[i].y = add_button.y + 28
            else:
                for i in range(2):
                    x = board_buttons.objects[move[i]].x
                    y = board_buttons.objects[move[i]].y
                    solution_tiles[i].x = x + 10
                    solution_tiles[i].y = y + 28
        else:
            for i in range(2):
                solution_tiles[i].x = -100
                solution_tiles[i].y = -100
        
    Button(game_window.objects, 300, 10, 80, 30, 'Next', solution_next_func, font = font)
    
solve_button = Button(game_window.objects, 300, 10, 80, 30, 'Solve', get_solution, font = font)

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
    board_buttons.clear_objects()
    selected = []
    window = "game"
Button(menu_window.objects, 150, 50, 100, 30, 'New Game', new_game, True, font = font)

def exit():
    global run
    run = False
Button(menu_window.objects, 150, 90, 100, 30, 'Exit', exit, font = font)

##  Game Over   ##
game_over_window = Window()
Button(game_over_window.objects, 20, 10, 100, 30, 'Menu', go_2_menu, font = font)
DisplayButton(game_over_window.objects, 110, 100, 180, 30, 'Game Over', font = font)
DisplayButton(game_over_window.objects, 110, 150, 180, 30, 'Final score: ', show_score, font = font)
Button(game_over_window.objects, 110, 200, 180, 30, 'New Game', new_game, True, font = font)

###############
## Game Loop ##
###############
run = True
window = "game"
while run:
    update_board()
    screen.fill((250, 218, 221)) # reset canvas

    # user imputs
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: # close the game
                run = False
            case pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 3: # right mouse button
                        selected = []
    # switch windows
    match window:
        case "game":
            game_window.run([screen, board.score])
            if board.game_over:
                window = "game_over"
        case "menu":
            menu_window.run([screen, board.score])
        case "game_over":
            game_over_window.run([screen, board.score])
        case _:
            game_window.run([screen, board.score])
    
    # update display window
    pygame.display.flip() # pygame.display.update(), but only part of the screen
    # pygame.display.update()

    # delay
    fpsClock.tick(fps)
pygame.quit()
sys.exit()