from sense_hat import SenseHat, ACTION_RELEASED
from time import sleep
from random import randrange
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

# Game parameters
SPEED=1                     # frames per second

# Data
shape = {                   # shapes of different blocks
    1: [[1,1],[1,1]],
    2: [[0,0,1],[1,1,1],[0,0,0]],
    3: [[1,1,1],[0,0,1],[0,0,0]],
    4: [[0,1,1],[1,1,0],[0,0,0]],
    5: [[1,1,0],[0,1,1],[0,0,0]],
    6: [[0,1,0],[1,1,1],[0,0,0]],
    7: [[0,0,0],[1,1,1],[0,0,0]]
}
color = {                   # colors of different blocks
    0: BLACK,
    1: GREEN,       # cube
    2: YELLOW,      # L
    3: BLUE,        # reverse L
    4: CYAN,        # flash
    5: WHITE,       # reverse flash
    6: MAGENTA,     # T
    7: RED          # long
}

def do_nothing(self):
    pass

class Game:
    def __init__(self):
        self.alive=True
        self.score=0
        self.field=self.Field()             # empty field
        self.block=self.Block()             # new block
        self.test_block=self.Block()        # used to check collisions before moving the real block
        self.test_block=copy.deepcopy(self.block)   # copy all properties of block to test block   
    def over(self):
        hat.show_message("Game Over!", text_colour=RED)
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
    def settle_block(self):                 # settle block into field, remove full lines, check for overflow and create new block
        self.score+=1
        for row in range(self.block.size):
            for column in range(self.block.size):
                if self.block.cells[row][column]>0:       # settle every solid cell of block
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
            self.settle_block()
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
            self.settle_block()
            self.refresh_display()

    class Field:
        def __init__(self):
            self.cells=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                        [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]  # 9 lines (line 0 invisible)
        def overflow(self):                     # check whether upper line is reached
            result=self.cells[0].count(0)
            if result<8:                        # line not empty?
                return True
            else:
                return False
        def remove_full_lines(self):
            for row in range(8,0,-1):
                while self.cells[row].count(0)==0: # no empty space
                    for line in range(row,0,-1):
                        self.cells[line]=copy.deepcopy(self.cells[line-1])     # replace line with line above
        def display(self):
            for row in range(1,9):
                for column in range(8):
                    hat.set_pixel(column, row-1, color[self.cells[row][column]])

    class Block:
        def __init__(self):
            self.type=randrange(1,8)
            self.cells=copy.deepcopy(shape[self.type])
            self.buffer_cells=copy.deepcopy(self.cells)              # buffer for rotation
            self.size=len(self.cells[0])
            for row in range(self.size):
                for column in range(self.size):
                    if self.cells[row][column]:
                        self.cells[row][column]=self.type    # assign color values to block
            self.xpos=3
            self.ypos=0
        def move_down(self):
            self.ypos+=1
        def move_left(self):
            self.xpos-=1
        def move_right(self):
            self.xpos+=1
        def rotate_left(self):
            for row in range(self.size):
                for column in range(self.size):
                    self.buffer_cells[row][column]=self.cells[self.size-1-column][row]
            self.cells=copy.deepcopy(self.buffer_cells)
        def rotate_right(self):
            for row in range(self.size):
                for column in range(self.size):
                    self.buffer_cells[row][column]=self.cells[column][self.size-1-row]
            self.cells=copy.deepcopy(self.buffer_cells)
        def display(self):
            for row in range(self.size):
                for column in range(self.size):
                    if self.cells[row][column]>0 and self.ypos+row>0:
                        hat.set_pixel(self.xpos+column, self.ypos+row-1, color[self.cells[row][column]])

# create objects
hat=SenseHat()
game=Game()

# configure joystick
hat.stick.direction_left = game.move_left
hat.stick.direction_right = game.move_right
hat.stick.direction_down = game.rotate_left
hat.stick.direction_up = game.rotate_right
hat.stick.direction_middle = game.drop

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