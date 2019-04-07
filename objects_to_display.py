import gameinfo
import random
from math import ceil

class Snake:
    '''Snake class holding information about the snake displayed on the screen'''
    RADIUS = 15
    SHOWABLE = ceil((gameinfo.WINDOW_HEIGHT - (gameinfo.WINDOW_HEIGHT / 2 + gameinfo.GAP)) / (RADIUS *  2))
    SPEED = 2
    INITIAL_X = int(gameinfo.WINDOW_WIDTH / 2)
    INITIAL_Y = int(gameinfo.WINDOW_HEIGHT / 2 + gameinfo.GAP)
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
            self.__last = [self.__last[0], self.__last[1] + Snake.RADIUS * 2] 
            self.a.append(self.__last)

    def blast(self):
        if self.l != 0:
            self.l -= 1
            if self.l > Snake.SHOWABLE: 
                self.__last = [self.__last[0], self.__last[1] + RADIUS * 2] 
                self.a.append(self.__last)
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
    MAX_PER_ROW = gameinfo.MAX_PER_ROW

    def __init__(self, free, lim):
        self.pos = 0
        self.passed = False
        self.a = [random.randint(1, lim) if random.randint(1, 11) % 5 == 0 else 0 for _ in range(Row.MAX_PER_ROW)]
        if free < 5:
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
        free = random.randint(1, 10)
        self.row.append(Row(free, s.l))

    def deleterow(self):
        self.row.pop()

    def advance(self, snake):
        for row in self.row:
            row.pos += snake.s
            if row.pos > 900:
                self.deleterow()
            if not row.passed:
                if row.pos >  Snake.TOUCH:
                    row.passed = True
                    for bk in range(MAX_PER_ROW):
                        if row[bk] != 0:
                            if BLOCKSTART[bk] < snake.head[0] < BLOCKEND[bk]:
                                snake.blast()
                                row[bk] -=  1
                                return True
                                break
        return False
                                

