from number import *

class Board:
    def __init__(self, int_list):
        self.content = []
        for i in range(len(int_list)):
            if i%9 == 0:
                self.content.append([])
            self.content[i//9].append(Number(int_list[i]))
    
    def __str__(self):
        string = ""
        for row in self.content:
            for number in row:
                string += str(number)
            string += '\n'
        return string
    
    def __getitem__(self, index):
        return self.content[index]