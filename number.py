class Number:
    def __init__(self, value):
        self.value = value
        self.gray = False
    
    def __str__(self):
        return str(self.value)
    
    def __add__(self, b):
        if type(b) is int:
            return self.value + b
        else:
            return self.value + b.value
    
    def __eq__(self, b):
        if type(b) is int:
            return self.value == b
        else:
            return self.value == b.value