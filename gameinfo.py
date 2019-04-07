import sdl2.ext as sdl

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 900
GAP = 80
COLOR_GRID =     {   "black":sdl.Color(0, 0, 0, 0), 
                     "white":sdl.Color(255, 255, 255, 0), 
                     "red":sdl.Color(255, 0, 0, 0), 
                     "green":sdl.Color(0, 255, 0, 0),
                     "white-green":sdl.Color(190, 255, 190, 0),
                     "blue":sdl.Color(0, 0, 255, 0),
                     "blue-green":sdl.Color(0, 255, 255, 0),
                     "red-blue":sdl.Color(255, 0, 255, 0)
                 }
MAX_PER_ROW = 5
BLOCK_GAP = 10
BLOCKSIZE = int(WINDOW_WIDTH / MAX_PER_ROW - BLOCK_GAP)
BLOCKSTART = [int((BLOCKSIZE * (i - 1)) + BLOCK_GAP * (i - 0.5)) for i in range(1, 6)]
BLOCKEND = [int(BLOCKSTART[i] + BLOCKSIZE) for i in range(5)]

