import gameinfo
import random
from math import ceil

class Snake:
    '''Snake class holding information about the snake displayed on the screen'''
    RADIUS = 15
    SHOWABLE = ceil((gameinfo.WINDOW_HEIGHT - (gameinfo.WINDOW_HEIGHT / 2 + gameinfo.GAP)) / (RADIUS *  2))
    SPEED = 2
    INITIAL_X = gameinfo.WINDOW_WIDTH / 2
    INITIAL_Y = gameinfo.WINDOW_HEIGHT / 2 + gameinfo.GAP
    INITIAL_LENGTH = 6
    TOUCH = INITIAL_Y - RADIUS

    def __init__(self):
        self.l = 1
        self.head = [Snake.INITIAL_X, Snake.INITIAL_Y]
        self.a = [self.head]
        self.s = Snake.SPEED
        self.__last = self.head
        self.collect(Snake.INITIAL_LENGTH - 1)

    def __str__(self):
        return "Snake [size - " + str(self.l) + "]"

    def collect(self, goodies):
        self.l += goodies
        for _ in range(goodies):
            if len(self.a) > Snake.SHOWABLE:
                break
            self.__last = [self.__last[0], self.__last[1] + RADIUS * 2] 
            self.a.append(self.__last)

    def blast(self):
        if self.l != 0:
            self.l -= 1
            self.a.remove(self.head)
            self.head = self.a[0]
            if self.l == 0:
                self.head = self.__last = None

    def move(self):
        st = len(self.a) - 1
        while st > 0:
            diff = self.a[st - 1][0] - self.a[st][0]
            if diff != 0:
                if diff > 0:
                    self.a[st][0] += 1
                else:
                    self.a[st][0] -= 1        
            st -= 1

class Row:
    '''One row of blocks as an obstruction to snake'''
    MAX_PER_ROW = 5
    TOL = 10
    SIZE = gameinfo.WINDOW_WIDTH / MAX_PER_ROW - TOL

    def __init__(self, free, lim):
        self.pos = 0
        self.passed = False
        self.a = [random.randint(1, lim) if random.randint(1, 2) % 2 == 0 else 0 for _ in range(MAX_PER_ROW)]
        self.a[free - 1] = 0

class BlockRows:
    '''The rows of blocks as an obstruction to snake'''
    MAX_PER_ROW = Row.MAX_PER_ROW
    def __init__(self):
        self.row = []
        self.__mountfirstrow()

    def __str__(self):
        return "A block row"

    def __mountfirstrow(self):
        free = random.randint(1, 5)
        self.row.append(Row(free, 5))

    def mountrow(self, s):
        free = random.randint(1, 5)
        self.row.append(Row(free, s.l))

    def deleterow(self):
        self.row.pop()

    def advance(self, snake):
        for row in self.row:
            row.pos += snake.s
            if not row.passed:
                if row.pos >  Snake.TOUCH:
                    row.passed = True
                    #check snake collision and take necessary action here.... 
                    #Also, the snake remains RADIUS units back after each blast, so take it forward instead of taking blocks backward
                    #Also, no need to take a free block way out, the snake can pass with hitting the block. That is in factv the rreal intension.....







