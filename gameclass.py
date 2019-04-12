#!/usr/bin/env python3

import gameinfo
import objects_to_display as ob
import sdl2
import sdl2.ext as sdl
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
           
    def renderall(self, snake, br, adjustenabled):
        self.__renderblockrows(br)
        self.rendersnake(snake)
        if self.mode == gameinfo.BLOCK_IN_MOTION:
            self.mode = br.advance(snake)
        else:
            self.mode = snake.advance(br)
        if adjustenabled:
            snake.adjust()

class Maingame:
    def __init__(self):
        self.r = Gamewindow()
        self.snake = ob.Snake()
        self.rows = ob.BlockRows()
    def Start(self):
        self.r.w.show()
        i = 0
        ad = True
        self.snake.collect(50)
        black = sdl.Color(0, 0, 0, 0)
        gamecondition = True
        while i < 50000 and gamecondition:
            self.r.clear(black)
            self.r.renderall(self.snake, self.rows, ad)
            ad = True
            e = sdl.get_events()
            for ev in e:
                if ev.type == sdl2.SDL_QUIT:
                    gamecondition = False
                    break
                elif ev.type == sdl2.SDL_KEYDOWN:
                    k = ev.key.keysym.sym
                    ad = False
                    if k == sdl2.SDLK_SPACE:
                        cond2 = True
                        while cond2:
                            extra = sdl.get_events()
                            for ex in extra:
                                if ex.type == sdl2.SDL_QUIT:
                                    cond2 = False
                                    gamecondition = False
                                elif ex.type == sdl2.SDL_KEYDOWN:
                                    if ex.key.keysym.sym == sdl2.SDLK_SPACE:
                                        cond2 = False
                    elif k == sdl2.SDLK_LEFT:
                        self.snake.move(True)
                    elif k == sdl2.SDLK_RIGHT:
                        self.snake.move(False)
                    break
            if self.snake.l < 2:
                self.snake.collect(20)
            self.r.present()
            i += 1

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

            

