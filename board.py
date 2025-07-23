import random

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
        self.add_count = 4 # can use board.add up to 4 times during a game.
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
    
    def get_legal_moves(self, index): # if there are bugs in this def, pray too god, couse there is no understanding this
        '''
        Return list with indexes of all possible moves there are that will result in numbers being grayed out from a tile (index)
        ----
        '''
        b1 = index
        list_of_moves = []
        def on_right_edge(i): return (i+1)%9 == 0

        # left & up
        for i in [1,9]:
            b = b1-i
            while b >=0 and self.content_flat()[b].gray:
                b -= i
            else:
                list_of_moves.append(b)
        # right & down
        for i in [1,9]:
            b = b1+i
            while b < len(self.content_flat()) and self.content_flat()[b].gray:
                b += i
            else:
                list_of_moves.append(b)
        # special case right (looping)
        if on_right_edge(b) and b != 8:
            b = b1 - 17
            while b < b1 and self.content_flat()[b].gray:
                b += 1
            else:
                list_of_moves.append(b)
        # diagonal
        for i in [-10, -8, 8, 10]:
            b = b1+i
            while b >= 0 and b < len(self.content_flat()) and self.content_flat()[b].gray:
                b+=i
            else:
                if not (on_right_edge(b) and i in [-10, 8]):
                    list_of_moves.append(b)
        return list_of_moves