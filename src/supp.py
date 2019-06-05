from mainclasses import *

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
        if "--help" in sys.argv:
            DisplayHelp()
            return 0
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
    sdl.init()
    ttf.TTF_Init()
    Maingame().Start(ischeck)
    sdl.quit()
    ttf.TTF_Quit()
    sdl2.SDL_Quit()
    return 0

def ResetScore():
    try:
        f = open("../support/.highscore", "rb+")
    except FileNotFoundError:
        f = open("../support/.highscore", "wb+")
    except:
        return
    f.seek(0)       # for safety
    f.write(int(0).to_bytes(20, 'big'))
    f.close()

def DisplayHighscore():
    try:
        f = open("../support/.highscore", "rb+")
    except FileNotFoundError:
        f = open("../support/.highscore", "wb+")
    except:
        return
    x = f.read()
    x = int.from_bytes(x, 'big')
    print("Highscore : %d" %x)
    f.close()




