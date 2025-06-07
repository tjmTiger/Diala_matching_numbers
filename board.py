from number import *  # noqa: F403
import random

class Board:
    def __init__(self):
        self.content = [[]]
        int_list = random.choices(range(1,9), k=35)
        for i in range(len(int_list)):
            if len(self.content[-1]) >= 9:
                self.content.append([])
            self.content[-1].append(Number(int_list[i]))  # noqa: F405
    
    def __str__(self):
        string = ""
        for row in self.content:
            for number in row:
                string += str(number)
            string += '\n'
        return string
    
    def __getitem__(self, index):
        return self.content[index]
    
    def add(self):
        int_list = [i for j in self.content for i in j if not i.gray] # flaten the list & remove gray numbers
        for i in range(len(int_list)):
            if len(self.content[-1]) >= 9:
                self.content.append([])
            self.content[-1].append(Number(int_list[i]))  # noqa: F405