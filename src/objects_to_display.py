'''
all the objects which are displayed on the screen are defined here
along with their methods
'''
import gameinfo
import random
from math import ceil

class Snake:
    '''Snake class holding information about the snake displayed on the screen'''
    RADIUS = gameinfo.SNAKERADIUS
    DIAMETER = RADIUS * 2
    SHOWABLE = ceil((gameinfo.WINDOW_HEIGHT - (gameinfo.WINDOW_HEIGHT / 2 + gameinfo.GAP)) / (RADIUS *  2))
    SPEED = gameinfo.INITIAL_SPEED
    INITIAL_X = int(gameinfo.WINDOW_WIDTH / 2)
    INITIAL_Y = int(gameinfo.WINDOW_HEIGHT / 2 + gameinfo.GAP)
    INITIAL_LENGTH = 6
    TOUCH = INITIAL_Y - RADIUS 
    PASS = INITIAL_Y + RADIUS + gameinfo.BLOCKSIZE 

    def __init__(self):
        self.l = 1
        self.score = 0
        self.head = [Snake.INITIAL_X, Snake.INITIAL_Y]
        self.a = [self.head]
        self.s = Snake.SPEED
        self.showable = Snake.SHOWABLE
        self.__last = self.head
        self.collect(Snake.INITIAL_LENGTH - 1)
        self.__moverow = 0
        self.moveability = True
        self.lasthead = self.head[0]

    def collect(self, goodies):
        '''called when snake takes the random bonus appeared on screen'''
        self.score += (goodies * 10)
        self.l += goodies
        for _ in range(goodies):
            self.__last = [self.__last[0], self.__last[1] + self.DIAMETER] 
            self.a.append(self.__last)

    def blast(self):
        '''
        called when snake touches any block the number on block 
        reduces by one and the snake head blasts making the 
        next body head when the snake length becomes 0, 
        the head becomes None
        '''
        if self.l != 0:
            self.score += 100
            self.l -= 1
            self.a.remove(self.head)
            if self.l == 0:
                self.head = self.__last = None
            else:
                self.head = self.a[0]

    def move(self, direction, M):
        '''
        moves the head to appropriate direction
        only moves if the moveability is True
        '''
        if self.moveability:
            if direction == gameinfo.LEFT:
                if self.l != 0 and self.head[0] > (2 * self.RADIUS):
                    self.head[0] -= (self.s * M)
            else:
                if self.l != 0 and self.head[0] < (gameinfo.WINDOW_WIDTH - 2 * self.RADIUS):
                    self.head[0] += (self.s * M)

    def adjust(self):
        '''
        adjusts the snake to stable form
        this function needs to be called with each iteration
        of the main loop
        when the snake head moves, this function attempts to 
        make the snake linear (Y-axis) again
        '''
        for i in range(0, len(self.a) - 1)[::-1]:
            self.a[i + 1][0] = self.a[i][0]
       
    def advance(self, brs):
        '''
        called when the game is in SNAKE_IN_MOTION mode
        it moves the snake up and the distance by which it moves
        is defined by the speed of the snake
        '''
        if self.l == 0:
            return gameinfo.GAME_OVER
        mode = gameinfo.SNAKE_IN_MOTION
        if (self.head[1] - self.s) <= Snake.INITIAL_Y:
            dist = self.head[1] - Snake.INITIAL_Y
            mode = gameinfo.BLOCK_IN_MOTION
        else:
            dist = self.s
        for body in self.a:
            body[1] -= dist
        for r in brs.row:
            if not r.passed:
                if (self.head[1] - self.RADIUS) <= r.pos:
                    for bk in range(len(r.a)):
                        if gameinfo.BLOCKSTART_IMG[bk] <= self.head[0] <= gameinfo.BLOCKEND_IMG[bk]:
                            if r.a[bk] != 0:
                                self.blast()
                                r.a[bk] -= 1
                                return gameinfo.SNAKE_IN_MOTION
                            else:
                                r.passed = True
        return mode

class Goody:
    '''Goodies which the snake would collect and eat to increase it's length'''
    __LEFT = Snake.INITIAL_X // Snake.DIAMETER + 1
    __RIGHT = (gameinfo.WINDOW_WIDTH - Snake.INITIAL_X) // Snake.DIAMETER + 1

    def __init__(self, n):
        self.num = n
        self.pos = 0
        self.val = [random.randint(1, 10) for _ in range(n)]
        self.co = [Snake.INITIAL_X + random.randint(0, Goody.__RIGHT) * Snake.DIAMETER if random.randint(1, 2) == 1 else Snake.INITIAL_X - random.randint(0, Goody.__LEFT) * Snake.DIAMETER for _ in range(n)]

class Row:
    '''One row of blocks as an obstruction to snake'''
    MAX_PER_ROW = gameinfo.MAX_PER_ROW

    def __init__(self, free, lim):
        self.pos = 0
        self.passed = False
        self.a = [random.randint(1, lim) if random.randint(1, 10) % 5 != 0 else 0 for _ in range(Row.MAX_PER_ROW)]
        self.a[free - 1] = random.randint(0, lim - gameinfo.TOLERANCE - 1)

class BlockRows:
    '''The rows of blocks as an obstruction to snake'''
    def __init__(self):
        self.row = []
        self.__mountfirstrow()

    def __mountfirstrow(self):
        '''called when initiating, mounts the first row of blocks'''
        free = random.randint(1, 6)
        self.row.append(Row(free, 6 + gameinfo.TOLERANCE))
        self.row[0].a[random.randint(0, gameinfo.MAX_PER_ROW - 1)] = 0

    def mountrow(self, s):
        '''called whenever a row of blocks needs to be mounted'''
        free = random.randint(1, Row.MAX_PER_ROW)
        self.row.insert(0, Row(free, s.l + gameinfo.TOLERANCE))

    def deleterow(self):
        '''deletes the oldest row'''
        self.row.pop()

    def advance(self, snake):
        '''
        called when the game is in BLOCK_IN_MOTION mode
        all the block rows move with the speed Snake.s
        in downward direction
        '''
        if snake.l == 0:
            return gameinfo.GAME_OVER
        for row in self.row:
            row.pos += snake.s
            if row.pos > (900 + gameinfo.BLOCKSIZE):
                self.deleterow()
            if not row.passed:
                if row.pos > Snake.TOUCH:
                    row.passed = True
                    for bk in range(Row.MAX_PER_ROW):
                        if row.a[bk] != 0:
                            if gameinfo.BLOCKSTART_IMG[bk] <= snake.head[0] <= gameinfo.BLOCKEND_IMG[bk]:
                                snake.blast()
                                row.a[bk] -=  1
                                row.passed = False
                                return gameinfo.SNAKE_IN_MOTION
                                break
        return gameinfo.BLOCK_IN_MOTION
                                

