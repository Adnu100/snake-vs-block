import gameinfo
import objects_to_display as ob
import sdl2
import sdl2.ext as sdl
from math import floor, sqrt

class Gamewindow(sdl.Renderer):
    def __init__(self):
        self.w = sdl.Window("Adnesh's Snake vs Block Game", (gameinfo.WINDOW_WIDTH, gameinfo.WINDOW_HEIGHT))
        sdl.Renderer.__init__(self, self.w)

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
                self.__renderblock(b, row.a[b], row.pos)

    def rendersnake(self, snake):
        self.color = gameinfo.COLOR_GRID["red-blue"]
        self.__rendercircle(snake.head[0], snake.head[1])
        for i in range(1, len(snake.a)):
            self.__rendercircle(snake.a[i][0], snake.a[i][1])
           
    def renderall(self, snake, br):
        self.__renderblockrows(br)
        self.rendersnake(snake)
        br.advance(snake)
        snake.move()

class Maingame:
    def __init__(self):
        self.r = Gamewindow()
        self.snake = ob.Snake()
        self.rows = ob.BlockRows()
    def Start(self):
        self.r.w.show()
        i = 0
        black = sdl.Color(0, 0, 0, 0)
        gamecondition = True
        while i < 50000 and gamecondition:
            self.r.clear(black)
            self.r.renderall(self.snake, self.rows)
            if i % 10000 == 0:
                self.rows.mountrow(self.snake)
            e = sdl.get_events()
            for ev in e:
                if ev.type == sdl2.SDL_QUIT:
                    gamecondition = False
                    break
            self.r.present()    

if __name__ == '__main__':
    Maingame().Start()

            

