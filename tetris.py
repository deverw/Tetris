from sense_hat import SenseHat, ACTION_RELEASED
from time import sleep
from random import randrange
import numpy as np
import copy

# Color definitions
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
CYAN=(0,255,255)
MAGENTA=(255,0,255)
WHITE=(255,255,255)
BLACK=(0,0,0)

SPEED=1                     # frames per second

shape = {                   # shapes of different blocks
    1: np.array([[1,1],[1,1]]),               # O
    2: np.array([[0,0,1],[1,1,1],[0,0,0]]),   # L
    3: np.array([[1,1,1],[0,0,1],[0,0,0]]),   # J
    4: np.array([[0,1,1],[1,1,0],[0,0,0]]),   # S
    5: np.array([[1,1,0],[0,1,1],[0,0,0]]),   # Z
    6: np.array([[1,1,1],[0,1,0],[0,0,0]]),   # T
    7: np.array([[0,0,0],[1,1,1],[0,0,0]])    # I
}
color = {                   # colors of different blocks
    0: BLACK,
    1: GREEN,       # O
    2: YELLOW,      # L
    3: BLUE,        # J
    4: CYAN,        # S
    5: WHITE,       # Z
    6: MAGENTA,     # T
    7: RED          # I
}

class Game:
    def __init__(self):
        self.alive=True
        self.score=0
        self.field=self.Field()             # empty field
        self.block=self.Block()             # new block
        self.test_block=copy.deepcopy(self.block)   # create copy of block including all prperties (used to check collisions before moving the real block) 
    def over(self):
        hat.show_message("Score: %s" % self.score, text_colour=GREEN)
        print("Score: %s" % self.score)
    def detect_collision(self):             # check whether test block collides with field elements or borders
        result=False
        for row in range(self.test_block.size):
            for column in range(self.test_block.size):
                if self.test_block.cells[row][column]>0:        # check every solid cell of test block
                    if self.test_block.xpos+column<0 or self.test_block.xpos+column>7 or self.test_block.ypos+row>8 or \
                       self.field.cells[self.test_block.ypos+row][self.test_block.xpos+column]>0:     # out of field range or collision
                        result=True
        return result           
    def land_block(self):                 # integrate block into field, remove full lines, check for overflow and create new block
        self.score+=1
        for row in range(self.block.size):
            for column in range(self.block.size):
                if self.block.cells[row][column]>0:       # don't integrate air
                    self.field.cells[self.block.ypos+row][self.block.xpos+column]=self.block.cells[row][column]
        self.field.remove_full_lines()
        if self.field.overflow():
            self.alive=False                # game over
        else:
            self.block.__init__()         # create new block
            self.test_block=copy.deepcopy(self.block)
    def refresh_display(self):
        self.field.display()
        self.block.display()
    def move_down(self):
        self.test_block.move_down()
        if self.detect_collision():
            self.land_block()
        else:
            self.block=copy.deepcopy(self.test_block)
        self.refresh_display()
    def move_left(self,event):
        if event.action != ACTION_RELEASED:
            self.test_block.move_left()
            if self.detect_collision():
                self.test_block=copy.deepcopy(self.block)
            else:
                self.block=copy.deepcopy(self.test_block)
            self.refresh_display()
    def move_right(self,event):
        if event.action != ACTION_RELEASED:
            self.test_block.move_right()
            if self.detect_collision():
                self.test_block=copy.deepcopy(self.block)
            else:
                self.block=copy.deepcopy(self.test_block)
            self.refresh_display()
    def rotate_left(self,event):
        if event.action != ACTION_RELEASED:
            self.test_block.rotate_left()
            if self.detect_collision():
                self.test_block=copy.deepcopy(self.block)
            else:
                self.block=copy.deepcopy(self.test_block)
            self.refresh_display()
    def rotate_right(self,event):
        if event.action != ACTION_RELEASED:
            self.test_block.rotate_right()
            if self.detect_collision():
                self.test_block=copy.deepcopy(self.block)
            else:
                self.block=copy.deepcopy(self.test_block)
            self.refresh_display()
    def drop(self,event):
        if event.action != ACTION_RELEASED:
            self.test_block.move_down()
            while not(self.detect_collision()):
                self.block=copy.deepcopy(self.test_block)
                self.refresh_display()
                self.test_block.move_down()
            self.land_block()
            self.refresh_display()

    class Field:
        def __init__(self):
            self.cells=np.zeros((9,8))          # empty field with 9 lines (line 0 invisible) and 8 columns
        def overflow(self):                     # check whether upper line is reached
            if np.count_nonzero(self.cells[0]):                        # upper line (invisible) not empty?
                return True
            else:
                return False
        def remove_full_lines(self):
            for row in range(8,0,-1):                           # from bottom to top
                while np.count_nonzero(self.cells[row])==8:     # line full
                    for line in range(row,0,-1):
                        self.cells[line]=self.cells[line-1]     # shift down all lines above and replace full line
        def display(self):
            for row in range(8):
                for column in range(8):
                    hat.set_pixel(column, row, color[self.cells[row+1][column]])

    class Block:
        def __init__(self):
            self.type=randrange(1,8)                           # one out of seven available shapes
            self.cells=np.copy(shape[self.type])
            self.size=np.size(self.cells,0)                    # determine size (one shape is 2x2 only)
            self.cells*=self.type                              # assign color code to block cells
            self.xpos=3
            self.ypos=0
        def move_down(self):
            self.ypos+=1
        def move_left(self):
            self.xpos-=1
        def move_right(self):
            self.xpos+=1
        def rotate_left(self):
            self.cells=np.rot90(self.cells)
        def rotate_right(self):
            self.cells=np.rot90(self.cells,3)
        def display(self):
            for row in range(self.size):
                for column in range(self.size):
                    if self.cells[row][column]>0 and self.ypos+row>0:
                        hat.set_pixel(self.xpos+column, self.ypos+row-1, color[self.cells[row][column]])

def do_nothing(self):
    pass

# create objects
hat=SenseHat()
game=Game()

# configure joystick
hat.stick.direction_left = game.move_left
hat.stick.direction_right = game.move_right
hat.stick.direction_up = game.rotate_right
hat.stick.direction_down = game.drop
hat.stick.direction_middle = game.rotate_left

# game loop
game.refresh_display()
while (game.alive):
    sleep(1/SPEED)
    game.move_down()

# remove joystick calls
hat.stick.direction_left = do_nothing
hat.stick.direction_right = do_nothing
hat.stick.direction_up = do_nothing
hat.stick.direction_down = do_nothing
hat.stick.direction_middle = do_nothing

game.over()