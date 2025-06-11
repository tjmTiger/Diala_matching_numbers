import random

class Number:
    def __init__(self, value):
        self.value = value
        self.gray = False
    
    def __str__(self):
        return str(self.value)
    
    def __add__(self, b):
        if type(b) is int:
            return self.value + b
        elif type(b) is str:
            return str(self.value) + b
        else:
            return self.value + b.value
    
    def __eq__(self, b):
        if type(b) is int:
            return self.value == b
        else:
            return self.value == b.value

class Board:
    def __init__(self, int_list = random.choices(range(1,10), k=35)):
        self.new_game(int_list)
    
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
    
    def add(self):
        int_list = [i for j in self.content for i in j if not i.gray] # flaten the list & remove gray numbers
        for i in range(len(int_list)):
            if len(self.content[-1]) >= 9:
                self.content.append([])
            self.content[-1].append(Number(int_list[i].value))

    def new_game(self, int_list = random.choices(range(1,10), k=35)):
        self.game_over = False
        self.score = 0
        self.content = [[]]
        for i in range(len(int_list)):
            if len(self.content[-1]) >= 9:
                self.content.append([])
            self.content[-1].append(Number(int_list[i]))

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