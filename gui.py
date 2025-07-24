# https://thepythoncode.com/article/make-a-button-using-pygame-in-python#:~:text=Now%20we%20can%20finally%20start,button%20will%20be%20pressed%20once.
import pygame

class Button():
    '''
    Button that can display a text and on click run a function
    ----
    '''
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

        self.buttonText = buttonText
        self.edit_buttonText(buttonText)
        objects.append(self)

    def edit_buttonText(self, text):
        # surface that contains the buttonText
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = pygame.font.SysFont(self.font[0], self.font[1]).render(text, True, (20, 20, 20))

    def process(self, info):
        '''
        Precesses the onclick funtion of the button. Should be run inside game loop
        ----
        '''
        screen = info[0]
        self.edit_buttonText(self.buttonText)
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
    '''
    Button that holds a Number displaying its state (gray) and value.
    Updates displayed value and state.
    ----
    '''
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
    '''
    Unclickable button for displaying text.
    ----
    '''
    def __init__(self, objects, x, y, width, height, buttonTextPermanent, buttonTextFunction=lambda:"",color = 'default' ,font = ['Arial', 40]):
        super().__init__(objects, x, y, width, height, buttonText =  buttonTextPermanent, font = font)
        self.buttonTextPermanent = buttonTextPermanent
        self.buttonTextFunction = buttonTextFunction
        if color != 'default':self.fillColors['normal'] = color
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
    '''
    "Div" for buttons. Used for displaying game board.
    ----
    '''
    def __init__(self, objects, x=0, y=0, width=0, height=0):
        super().__init__(objects, x, y, width, height)
        self.objects = []
    
    def __del__(self):
        self.clear_objects()
    
    def process(self, info):
        for object in self.objects:
            object.process(info)
    
    def clear_objects(self):
        '''
        Remove all buttons that this group contains.
        ----
        '''
        for i in self.objects.copy():
            self.objects.remove(i)
            del i
        self.objects = []

    def adjacent(self, board, button1, button2):
        return board.adjacent(self.objects.index(button1), self.objects.index(button2))

class Window:
    def __init__(self):
        self.objects = []
    
    def run(self, info):
        for object in self.objects:
            object.process(info)