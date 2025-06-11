# https://thepythoncode.com/article/make-a-button-using-pygame-in-python#:~:text=Now%20we%20can%20finally%20start,button%20will%20be%20pressed%20once.
import pygame

class Button():
    def __init__(self, objects, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False, font = ['Arial', 40]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#FF99C7',
            'pressed': '#E75480',
        }
        self.font = font

        self.edit_buttonText(buttonText)
        objects.append(self)

    def edit_buttonText(self, text):
        # surface that contains the buttonText
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = pygame.font.SysFont(self.font[0], self.font[1]).render(text, True, (20, 20, 20))

    def process(self, info):
        screen = info[0]
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        # blitting the text onto the buttonSurface and then this surface onto the screen
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

class NumberButton(Button):
    def __init__(self, objects, x, y, width, height, number, onclickFunction=None, onePress=False, font = ['Arial', 40]):
        super().__init__(objects, x, y, width, height, buttonText=str(number), onclickFunction=onclickFunction, onePress=onePress, font = font)
        self.fillColors['gray'] = '#666666'
        self.number = number

    def process(self, info):
        screen = info[0]
        mousePos = pygame.mouse.get_pos()
        if self.number.gray:
            self.buttonSurface.fill(self.fillColors['gray'])
        else:
            self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction(self)
                elif not self.alreadyPressed:
                    self.onclickFunction(self)
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        # blitting the text onto the buttonSurface and then this surface onto the screen
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

class DisplayButton(Button):
    def __init__(self, objects, x, y, width, height, buttonTextPermanent, buttonTextFunction=lambda:"", font = ['Arial', 40]):
        super().__init__(objects, x, y, width, height, buttonText =  buttonTextPermanent, font = font)
        self.buttonTextPermanent = buttonTextPermanent
        self.buttonTextFunction = buttonTextFunction
        # self.edit_buttonText(self.buttonTextPermanent + str(self.buttonTextChanging))
    
    def process(self,info):
        screen = info[0]
        self.edit_buttonText(self.buttonTextPermanent + self.buttonTextFunction())
        self.buttonSurface.fill(self.fillColors['normal'])
        # blitting the text onto the buttonSurface and then this surface onto the screen
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


class ButtonGroup(Button):
    def __init__(self, objects, x=0, y=0, width=0, height=0):
        super().__init__(objects, x, y, width, height)
        self.objects = []
    
    def process(self, info):
        for object in self.objects:
            object.process(info)
    
    def objects_flat(self):
        return [i for j in self.objects for i in j]
    
    def clear_objects(self):
        for i in self.objects.copy():
            self.objects.remove(i)
            del i
        self.objects = []

    def adjacent(self, button1, button2): # if there are bugs in this def, pray too god, couse there is no understanding this
        gray_buttons = []
        for b in range(len(self.objects)):
            if self.objects[b].number.gray:
                gray_buttons.append(b)
                
        b1 = self.objects.index(button1)
        b2 = self.objects.index(button2)

        # logic
        def on_right_edge(i): return (i+1)%9 == 0

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
            while b <= len(self.objects) and b in gray_buttons:
                b += i
            else:
                if b == b2:
                    return True
        # special case horisontal right (looping)
        if on_right_edge(b) and b != 8:
            b = b1 - 17
            while b < b1 and b in gray_buttons:
                b += 1
            else:
                if b == b2:
                    return True
        # diagonal
        for i in [-10, -8, 8, 10]:
            b = b1+i
            while b >= 0 and b <= len(self.objects) and b in gray_buttons:
                b+=i
            else:
                if b == b2 and not (on_right_edge(b) and i in [-10, 8]):
                    return True
        return False

class Window:
    def __init__(self):
        self.objects = []
    
    def run(self, info):
        for object in self.objects:
            object.process(info)