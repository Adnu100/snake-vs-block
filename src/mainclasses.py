import gameinfo
import objects_to_display as ob
import sdl2
import sdl2.ext as sdl
import sdl2.sdlttf as ttf
import random
import sys
from math import floor, sqrt

class Gamewindow(sdl.Renderer):
    YELLOW = sdl2.SDL_Color(255, 255, 0, 0)
    WHITE = sdl2.SDL_Color(255, 255, 255, 0)
    BLACK = sdl2.SDL_Color(0, 0, 0, 0)
    Rscore = sdl2.SDL_Rect(0, 0, 250, 50)

    def __init__(self):
        self.w = sdl.Window("Adnesh's Snake vs Block Game", (gameinfo.WINDOW_WIDTH, gameinfo.WINDOW_HEIGHT))
        sdl.Renderer.__init__(self, self.w)
        self.mode = gameinfo.BLOCK_IN_MOTION
        self.t = ttf.TTF_OpenFont(b"../support/font.ttf", 30)

    def __rendercircle(self, xc, yc, r = ob.Snake.RADIUS):
        for x in range(r): 
            y = floor(sqrt(r ** 2 - x ** 2))
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
        self.fill((sx, y - gameinfo.BLOCKSIZE, gameinfo.BLOCKSIZE, gameinfo.BLOCKSIZE))
        texttodisplay = "%2d" %val
        sur = ttf.TTF_RenderText_Solid(self.t, texttodisplay.encode(), self.BLACK)
        tex = sdl2.SDL_CreateTextureFromSurface(self.sdlrenderer, sur)
        Rblock = sdl2.SDL_Rect(sx + gameinfo.RECTSTART_X, y - gameinfo.RECTSTART_Y, gameinfo.RECTWIDTH, gameinfo.RECTHEIGHT)
        sdl2.SDL_RenderCopy(self.sdlrenderer, tex, None, Rblock)
        sdl2.SDL_FreeSurface(sur)
        sdl2.SDL_DestroyTexture(tex)

    def __renderblockrows(self, br):
        for row in br.row:
            for b in range(ob.Row.MAX_PER_ROW):
                if row.a[b] != 0:
                    self.__renderblock(b, row.a[b], row.pos)

    def rendersnake(self, snake):
        if snake.l > 0:
            self.color = gameinfo.COLOR_GRID["red-blue"]
            for i in range(0, len(snake.a)):
                self.__rendercircle(snake.a[i][0], snake.a[i][1])
                if i > ob.Snake.SHOWABLE:
                    break
            sur = ttf.TTF_RenderText_Solid(self.t, snake.l.__str__().encode(), self.WHITE)
            tex = sdl2.SDL_CreateTextureFromSurface(self.sdlrenderer, sur)
            Rsnake = sdl2.SDL_Rect(snake.head[0] - gameinfo.TSPACE_X, snake.head[1] - gameinfo.TSPACE_Y, gameinfo.TWIDTH, gameinfo.THEIGHT)
            sdl2.SDL_RenderCopy(self.sdlrenderer, tex, None, Rsnake)
            sdl2.SDL_FreeSurface(sur)
            sdl2.SDL_DestroyTexture(tex)

    def rendergoodies(self, g_row):
        self.color = sdl.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0)
        for r in g_row:
            for g in range(r.num):
                self.__rendercircle(r.co[g], r.pos, gameinfo.BONUSRADIUS)
           
    def renderall(self, snake, br, g):
        self.__renderblockrows(br)
        self.rendersnake(snake)
        self.rendergoodies(g)
        if self.mode == gameinfo.BLOCK_IN_MOTION:
            self.mode = br.advance(snake)
            for gd in g:
                gd.pos += snake.s
                if gd.pos > gameinfo.WINDOW_HEIGHT:
                    g.remove(gd)
        else:
            self.mode = snake.advance(br)
        texttodisplay = "score:" 
        texttodisplay += "%8d" %snake.score
        texttodisplay = texttodisplay.encode()
        sur = ttf.TTF_RenderText_Solid(self.t, texttodisplay, self.YELLOW)
        tex = sdl2.SDL_CreateTextureFromSurface(self.sdlrenderer, sur)
        sdl2.SDL_RenderCopy(self.sdlrenderer, tex, self.Rscore, self.Rscore)
        sdl2.SDL_FreeSurface(sur)
        sdl2.SDL_DestroyTexture(tex)
        snake.adjust()

class Maingame:
    def __init__(self):
        self.r = Gamewindow()
        self.snake = ob.Snake()
        self.rows = ob.BlockRows()
        self.g = []

    def Start(self, ischeck):
        self.r.w.show()
        Running = True
        i = 0
        scoreholder = sdl2.SDL_Rect(0, 0, 200, 200)
        score = 0
        lim = random.randint(gameinfo.BLOCKSIZE, 900)
        d = 0
        delay_ = gameinfo.DELAY1
        while Running:
            C = sdl2.SDL_GetTicks()
            if self.snake.head == None:
                Running =  False
            i += 1
            self.r.clear(gameinfo.COLOR_GRID["black"])
            self.r.renderall(self.snake, self.rows, self.g)
            events = sdl.get_events()
            for e in events:
                if e.type == sdl2.SDL_QUIT:
                    Running = False
                    break
                elif e.type == sdl2.SDL_KEYDOWN and self.snake.head != None:
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
                        if self.snake.l != 0 and self.snake.head[0] < (gameinfo.WINDOW_WIDTH - 2 * ob.Snake.RADIUS):
                            self.snake.move(False)
                    elif k == sdl2.SDLK_LEFT and self.snake.head[0] > (0 + 2 * ob.Snake.RADIUS):
                        if self.snake.l != 0:
                            self.snake.move(True)
            if self.rows.row:
                if self.rows.row[0].pos > lim:
                    self.rows.mountrow(self.snake)
                    lim = random.randint(gameinfo.BLOCKSIZE, 900) 
                random.seed(random.random())
                if random.randint(1, 500) == random.randint(1, 500) and self.rows.row[0].pos > gameinfo.BLOCKSIZE:
                    goody = ob.Goody(random.randint(1, 3))
                    self.g.append(goody)
            else:
                self.rows.mountrow(self.snake)
            #if len(sys.argv) > 1 and "--check" in sys.argv:
            if ischeck:
                if self.snake.l == 1:
                    self.snake.collect(6)
            if self.snake.head != None:
                for h in self.g:
                    if h.pos > (self.snake.head[1] + self.snake.RADIUS) or h.pos < (self.snake.head[1] - self.snake.RADIUS):
                        continue
                    for c in range(len(h.co)):
                        if h.co[c] == self.snake.head[0]:
                            val = h.val[c]
                            h.co.remove(h.co[c])
                            h.val.remove(h.val[c])
                            self.snake.collect(val)
                            h.num -= 1
                            if h.num == 0:
                                self.g.remove(h)
                            break
            if (self.snake.score - d) > gameinfo.SCORE_DIFF:
                d = self.snake.score
                if delay_ == gameinfo.DELAY1:
                    self.snake.s += 1
                    delay_ = gameinfo.DELAY2
                elif delay_ == gameinfo.DELAY2:
                    delay_ = gameinfo.DELAY1
            delay = sdl2.SDL_GetTicks() - C
            #print(delay)
            if delay < delay_:
                sdl2.SDL_Delay(delay_ - delay)
            self.r.present()
        self.r.w.hide()
        self.__printscore()
    
    def __printscore(self):
        score = self.snake.score
        try:
            f = open("../support/.highscore", "rb+")
        except FileNotFoundError:
            f = open("../support/.highscore", "wb+")
        except:
            return
        x = f.read()
        if x: 
            hs = int.from_bytes(x, 'big')
            if score < hs:
                print("\tUpps!")
                print("\tscore : " + score.__str__())
                print("\t(Highscore : %d)" %hs)
            else:
                print("\tCongrats!! New Highscore!!!")
                print("\tscore : " + score.__str__())
                f.seek(0)
                f.write(score.to_bytes(20, 'big'))
        else:
            f.write(score.to_bytes(20, 'big'))
            print("\tCongrats!! New Highscore!!!")
            print("\tscore : " + score.__str__())
        f.close()

def StartGame():
    # handling command line arguments with an unstandard way 
    # because there are may few options and they do not
    # affect time complexity
    ischeck = False
    if len(sys.argv) > 1:
        if "--check" in sys.argv:
            ischeck = True
        else:
            ischeck = False
        if "--reset" in sys.argv:
            ResetScore()
            return 0
        if "--score" in sys.argv:
            DisplayHighscore()
            return 0
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
    sdl.init()
    ttf.TTF_Init()
    Maingame().Start(ischeck)
    sdl.quit()
    ttf.TTF_Quit()
    sdl2.SDL_Quit()
    return 0

