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

    def __str__(self):
        return "Snake [size - " + str(self.l) + "]"

    def collect(self, goodies):
        self.score += (goodies * 10)
        self.l += goodies
        for _ in range(goodies):
            self.__last = [self.__last[0], self.__last[1] + Snake.RADIUS * 2] 
            self.a.append(self.__last)

    def blast(self):
        if self.l != 0:
            self.score += 100
            self.l -= 1
            self.a.remove(self.head)
            if self.l == 0:
                self.head = self.__last = None
            else:
                self.head = self.a[0]

    def move(self, direction, M):
        if self.moveability:
            if direction == gameinfo.LEFT:
                if self.l != 0 and self.head[0] > (2 * self.RADIUS):
                    self.head[0] -= (self.s * M)
            else:
                if self.l != 0 and self.head[0] < (gameinfo.WINDOW_WIDTH - 2 * self.RADIUS):
                    self.head[0] += (self.s * M)

    def adjust(self):
        for i in range(0, len(self.a) - 1)[::-1]:
            self.a[i + 1][0] = self.a[i][0]
       
    def advance(self, brs):
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

    def __str__(self):
        return "A block row"

    def __mountfirstrow(self):
        free = random.randint(1, 6)
        self.row.append(Row(free, 6 + gameinfo.TOLERANCE))
        self.row[0].a[random.randint(0, gameinfo.MAX_PER_ROW - 1)] = 0

    def mountrow(self, s):
        free = random.randint(1, Row.MAX_PER_ROW)
        self.row.insert(0, Row(free, s.l + gameinfo.TOLERANCE))

    def deleterow(self):
        self.row.pop()

    def advance(self, snake):
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
                                

