import random

class Number:
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
    def __init__(self, int_list = random.choices(range(1,10), k=35)):
        self.new_game(int_list)

    def new_game(self, int_list = random.choices(range(1,10), k=35)):
        self.game_over = False
        self.add_count = 4 # can use board.add up to 4 times during a game.
        self.score = 0
        self.content = [[]]
        for i in range(len(int_list)):
            if len(self.content[-1]) >= 9:
                self.content.append([])
            self.content[-1].append(Number(int_list[i]))
    
    def __str__(self):
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
        return len(self.content)
    
    def get_legal_moves(self):
        return 0
    
    def add(self):
        if self.add_count > 0:
            int_list = [i for j in self.content for i in j if not i.gray] # flaten the list & remove gray numbers
            for i in range(len(int_list)):
                if len(self.content[-1]) >= 9:
                    self.content.append([])
                self.content[-1].append(Number(int_list[i].value))
            self.add_count -= 1

    def remove_gray_rows(self):
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
        return [i for j in self.content for i in j]
    
    def adjacent(self, index1, index2):
        b1 = index1
        b2 = index2
        def on_right_edge(i): return (i+1)%9 == 0

        # horisontal left & vertical up
        for i in [1,9]:
            b = b1-i
            while b >=0 and self.content_flat()[b].gray:
                b -= i
            else:
                if b == b2:
                    return True
        # horisontal right & vertical down
        for i in [1,9]:
            b = b1+i
            while b < len(self.content_flat()) and self.content_flat()[b].gray:
                b += i
            else:
                if b == b2:
                    return True
        # special case horisontal right (looping)
        if on_right_edge(b) and b != 8:
            b = b1 - 17
            while b < b1 and self.content_flat()[b].gray:
                b += 1
            else:
                if b == b2:
                    return True
        # diagonal
        for i in [-10, -8, 8, 10]:
            b = b1+i
            while b >= 0 and b < len(self.content_flat()) and self.content_flat()[b].gray:
                b+=i
            else:
                if b == b2 and not (on_right_edge(b) and i in [-10, 8]):
                    return True
        return False