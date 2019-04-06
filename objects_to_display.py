import sdl2
import sdl2.ext as sdl
import random
from math import ceil

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 900
GAP = 80
COLOR_GRID =     {   "black":sdl.Color(0, 0, 0, 0), 
                     "white":sdl.Color(255, 255, 255, 0), 
                     "red":sdl.Color(255, 0, 0, 0), 
                     "green":sdl.Color(0, 255, 0, 0),
                     "white-green":sdl.Color(190, 255, 190, 0),
                     "blue":sdl.Color(0, 0, 255, 0),
                     "blue-green":sdl.Color(0, 255, 255, 0)
                 }


class Snake():
    RADIUS = 15
    SHOWABLE = ceil((WINDOW_HEIGHT - (WINDOW_HEIGHT / 2 + GAP)) / (RADIUS *  2))
    SPEED = 2
    INITIAL_X = WINDOW_WIDTH / 2
    INITIAL_Y = WINDOW_HEIGHT / 2 + GAP
    INITIAL_LENGTH = 6
    def __init__(self):
        self.l = 1
        self.head = [INITIAL_X, INITIAL_Y]
        self.__a = [self.head]
        self.s = SPEED
        self.last = self.head
        self.collect(INITIAL_LENGTH - 1)
    def __str__(self):
        return "Snake [size - " + str(self.l) + "]"
    def collect(self, goodies):
        self.l += goodies
        for _ in range(goodies):
            if len(self.__a) > SHOWABLE:
                break
            self.last = [self.last[0], self.last[1] + RADIUS * 2] 
            self.__a.append(self.last)
    def blast(self):
        if self.l != 0:
            self.l -= 1
            self.__a.remove(self.head)
            self.head = self.a[0]
            if self.l == 0:
                self.head = self.last = None
    def move(self):
        st = len(self.__a) - 1
        while st > 0:
            diff = self.__a[st - 1][0] - self.__a[st][0]
            if diff != 0:
                if diff > 0:
                    self.__a[st][0] += 1
                else:
                    self.__a[st][0] -= 1        
            st -= 1

class BlockRow():
    MAX_PER_ROW = 5
    TOL = 10
    SIZE = WINDOW_WIDTH / MAX_PER_ROW - TOL
    COLORBLEACH = (COLOR_GRID["white-green"], COLOR_GRID["green"], COLOR_GRID["blue"], COLOR_GRID["blue-green"], COLOR_GRID["red"])

