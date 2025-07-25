import random
import copy

class Number:
    '''
    Tiles used in board. Contain tile value and if its gray
    ----
    '''
    def __init__(self, value, gray = False):
        self.value = value
        self.gray = gray
    
    def __str__(self):
        return str(self.value)
    
    def __add__(self, b):
        if type(b) is int:
            return self.value + b
        elif type(b) is str:
            return str(self.value) + b
        else:
            return self.value + b.value
        
    def __sub__(self, b):
        if type(b) is int:
            return self.value - b
        else:
            return self.value - b.value
    
    def __eq__(self, b):
        if type(b) is int:
            return self.value == b
        else:
            return self.value == b.value

class Board:
    '''
    Object with information of tiles and some game rules
    ----
    '''
    def __init__(self, int_list = random.choices(range(1,10), k=35)):
        # OBS! for new game option to work correctly, place all initializations in "new_game" function below!
        self.new_game(int_list)

    def new_game(self, int_list = random.choices(range(1,10), k=35)):
        '''
        Reset state of the board
        ----
        '''
        self.game_over = False
        self.add_count = 5 # can use board.add up to 5 times during a game.
        self.score = 0
        self.content = [[]]
        for i in range(len(int_list)):
            if len(self.content[-1]) >= 9:
                self.content.append([])
            self.content[-1].append(Number(int_list[i]))
    
    def __str__(self):
        '''
        Value of tiles as a string
        ----
        '''
        string = ""
        for row in self.content:
            for number in row:
                if number.gray:
                    string += '\033[90m' + str(number) + '\033[0m'
                else: 
                    string += str(number)
            string += '\n'
        return string
    
    def __getitem__(self, index):
        return self.content[index]
    
    def __len__(self):
        '''
        Return number of rows in a board
        ----
        '''
        return len(self.content)
    
    def add(self):
        '''
        Add extra row at the end. Can be used max 4 times during a game.
        ----
        '''
        if self.add_count > 0:
            int_list = [i for j in self.content for i in j if not i.gray] # flaten the list & remove gray numbers
            for i in range(len(int_list)):
                if len(self.content[-1]) >= 9:
                    self.content.append([])
                self.content[-1].append(Number(int_list[i].value))
            self.add_count -= 1

    def remove_gray_rows(self):
        '''
        Remove completed rows
        ----
        '''
        new_content = []
        for row in range(len(self.content)):
            for num in self.content[row]:
                if not num.gray:
                    new_content.append(self.content[row])
                    break
        removed = len(self.content) - len(new_content)
        self.score += removed*10 # 10 points per removed row
        self.content = new_content
        if len(self.content) == 0 and not self.game_over:
            self.score += 180
            self.game_over = True
        return removed > 0
    
    def content_flat(self):
        '''
        Return the 2D content list as a 1D content list
        ----
        '''
        return [i for j in self.content for i in j]
    
    def adjacent(self, index1, index2):
        '''
        Check if two tiles can be grayed out.
        ----
        '''
        if index2 in self.get_legal_moves(index1):
            return True
        return False
    
    def get_legal_moves(self, index1): # if there are bugs in this def, pray too god, couse there is no understanding this
        '''
        Return list with indexes of all possible moves there are that will result in numbers being grayed out from a tile (index)
        Todo: we r checking twice if numbers are connectable, once in here, and secound time in main, should fix that.
        ----
        '''
        def on_right_edge(i): return (i+1)%9 == 0
        def on_left_edge(i): return i%9 == 0
        def not_diagonal_jumping(index, i):
            return (not (on_right_edge(index) and i in [-10, 8]) and not (on_left_edge(index) and i in [10, -8]))
        def connectable(i1, i2):
            if i2 >= 0 and i2 < len(self.content_flat()):
                value1 = self.content_flat()[i1].value
                value2 = self.content_flat()[i2].value
                return (value1 == value2 or value1+value2 == 10)
            return False
        list_of_moves = []
        # left & up
        for i in [1,9]:
            index = index1-i
            if index < 0:
                break
            while index >=0 and self.content_flat()[index].gray:
                index -= i
            else:
                if connectable(index1, index):
                    list_of_moves.append(index)
        # right & down
        for i in [1,9]:
            index = index1+i
            if index >= len(self.content_flat()):
                break
            while index < len(self.content_flat()) and self.content_flat()[index].gray:
                index += i
            else:
                if connectable(index1, index):
                    list_of_moves.append(index)
        # special case right (looping)
        if on_right_edge(index) and index != 8:
            index = index1 - 17
            while index < index1 and self.content_flat()[index].gray:
                index += 1
            else:
                if index >= 0 and connectable(index1, index):
                    list_of_moves.append(index)
        # diagonal
        for i in [-10, -8, 8, 10]:
            index = index1+i
            while index >= 0 and index < len(self.content_flat()) and self.content_flat()[index].gray and not_diagonal_jumping(index, i):
                index+=i
            else:
                if connectable(index1, index) and not_diagonal_jumping(index, i):
                    list_of_moves.append(index)
        return list_of_moves
    
    def get_all_legal_moves(self):
        list_of_moves = []
        for index in range(len(self.content_flat())): # loop throgh all indexes of Numbers in board
            if not self.content_flat()[index].gray:
                for index2 in self.get_legal_moves(index):
                    if index2 > index and not self.content_flat()[index2].gray: # avoid duplicates ([index, index2] and [index2, index] are the same moves), by only looking forward, we avoid this dupe
                        list_of_moves.append([index, index2])
        if self.add_count > 0:
            list_of_moves.append(["+"])
        return list_of_moves


    # Solving the game
    def find_solution(self):
        def game_won(board):
            if not board.content_flat():
                return True
            return False
        
        def add_descendants(board, depth = 0):
            legal_moves = board.get_all_legal_moves()
            if legal_moves:
                for move in legal_moves:
                    new_board = copy.deepcopy(board)
                    if move == ["+"]:
                        new_board.add()
                    else:
                        new_board.content_flat()[move[0]].gray = True
                        new_board.content_flat()[move[1]].gray = True
                    new_board.remove_gray_rows()
                    result = add_descendants(new_board, depth+1)
                    # print(depth)
                    if result["win"]:
                        result["moves"].insert(0, move)
                        return result
                return {"win": False, "moves": []}
            else:
                if game_won(board):
                    return {"win": True, "moves": []}
                else:
                    return {"win": False, "moves": []}
        result = add_descendants(copy.deepcopy(self))
        """
        moves = result["moves"]
        converted_moves = []
        for move in moves:
            if not move[0] == "+":
                converted_moves.append([move[0]%9, move[0]//9, move[1]%9, move[1]//9])
            else: converted_moves.append(["+"])
        return converted_moves
        """
        return result