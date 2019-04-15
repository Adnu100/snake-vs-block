#!/usr/bin/env python3

import gameinfo
import objects_to_display as ob
import sdl2
import sdl2.ext as sdl
import random
from math import floor, sqrt

class Gamewindow(sdl.Renderer):
    def __init__(self):
        self.w = sdl.Window("Adnesh's Snake vs Block Game", (gameinfo.WINDOW_WIDTH, gameinfo.WINDOW_HEIGHT))
        self.i = 0
        sdl.Renderer.__init__(self, self.w)
        self.mode = gameinfo.BLOCK_IN_MOTION

    def __rendercircle(self, xc, yc):
        for x in range(ob.Snake.RADIUS): 
            y = floor(sqrt(ob.Snake.RADIUS ** 2 - x ** 2))
            self.draw_line((xc + x, yc + y, xc + x, yc - y))
            self.draw_line((xc - x, yc + y, xc - x, yc - y))

    def __renderblock(self, number, val, y):
        if 0 < val < 10:
            self.color = gameinfo.COLOR_GRID["white-green"]
        elif 9 < val < 20:
            self.color = gameinfo.COLOR_GRID["green"]
        elif 19 < val < 30:
            self.color = gameinfo.COLOR_GRID["blue-green"]
        elif 29 < val < 40:
            self.color = gameinfo.COLOR_GRID["blue"]
        else:
            self.color = gameinfo.COLOR_GRID["red"]
        sx = gameinfo.BLOCKSTART[number]
        ex = gameinfo.BLOCKEND[number]
        for i in range(gameinfo.BLOCKSIZE):
            self.draw_line((sx, y - i, ex, y - i))

    def __renderblockrows(self, br):
        for row in br.row:
            for b in range(ob.Row.MAX_PER_ROW):
                if row.a[b] != 0:
                    self.__renderblock(b, row.a[b], row.pos)

    def rendersnake(self, snake):
        self.color = gameinfo.COLOR_GRID["red-blue"]
        for i in range(0, len(snake.a)):
            self.__rendercircle(snake.a[i][0], snake.a[i][1])
            if i > ob.Snake.SHOWABLE:
                break
           
    def renderall(self, snake, br):
        self.__renderblockrows(br)
        self.rendersnake(snake)
        if self.mode == gameinfo.BLOCK_IN_MOTION:
            self.mode = br.advance(snake)
        else:
            self.mode = snake.advance(br)
        snake.adjust(True)

class Maingame:
    def __init__(self):
        self.r = Gamewindow()
        self.snake = ob.Snake()
        self.rows = ob.BlockRows()
    def Start(self):
        self.r.w.show()
        Running = True
        i = 0
        lim = random.randint(gameinfo.BLOCKSIZE, 900)
        while Running:
            i += 1
            self.r.clear(gameinfo.COLOR_GRID["black"])
            self.r.renderall(self.snake, self.rows)
            events = sdl.get_events()
            for e in events:
                if e.type == sdl2.SDL_QUIT:
                    Running = False
                    break
                elif e.type == sdl2.SDL_KEYDOWN:
                    k = e.key.keysym.sym
                    if k == sdl2.SDLK_SPACE:
                        while Running:
                            events_ext = sdl.get_events()
                            for e in events_ext:
                                if e.type == sdl2.SDL_KEYDOWN:
                                    Running = False
                                    break
                        Running = True
                    elif k == sdl2.SDLK_RIGHT:
                        if self.snake.l != 0:
                            self.snake.move(False)
                    elif k == sdl2.SDLK_LEFT:
                        if self.snake.l != 0:
                            self.snake.move(True)
            self.r.present()
            if self.rows.row[0].pos > lim:
                self.rows.mountrow(self.snake)
                lim = random.randint(gameinfo.BLOCKSIZE, 900)
        self.r.w.hide()

def StartGame():
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
    sdl.init()
    Maingame().Start()
    sdl.quit()
    sdl2.SDL_Quit()

if __name__ == '__main__':
    StartGame()
    #i = Maingame()
    #i.Start()

            

