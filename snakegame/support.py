'''main functions required in backend are defined here'''

from .mainclasses import *

def StartGame():
    '''
    The function which handles the command line arguments,
    initialises SDL2 and TTF, initiates the MainGame class 
    and invokes its Start() function
    after that, it closes the SDL2 and TTF
    returns 0 after successful execution
    '''
    repete = ischeck = False
    if len(sys.argv) > 1:
        if "--check" in sys.argv or "-c" in sys.argv:
            ischeck = True
        else:
            ischeck = False
        if "--reset" in sys.argv or "-r" in sys.argv:
            ResetScore()
            return 0
        if "--score" in sys.argv or "-s" in sys.argv:
            DisplayHighscore()
            return 0
        if "--help" in sys.argv or "-h" in sys.argv:
            DisplayHelp()
            return 0
        if "--repete" in sys.argv or "-R" in sys.argv:
            repete = True
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
    sdl.init()
    ttf.TTF_Init()
    Maingame().Start(ischeck, repete)
    sdl.quit() 
    ttf.TTF_Quit()
    sdl2.SDL_Quit()
    return 0

def ResetScore():
    '''resets the highscore'''
    try:
        f = open("support/.highscore", "rb+")
    except FileNotFoundError:
        f = open("support/.highscore", "wb+")
    except:
        return
    f.seek(0)       # for safety
    f.write(int(0).to_bytes(20, 'big'))
    f.close()

def DisplayHighscore():
    '''displays the highscore on terminal'''
    try:
        f = open("support/.highscore", "rb+")
    except FileNotFoundError:
        f = open("support/.highscore", "wb+")
    except:
        return
    x = f.read()
    x = int.from_bytes(x, 'big')
    print("Highscore : %d" %x)
    f.close()

def DisplayHelp():
    '''
    displays help on the terminal
    (it prints the help.txt file in support directory)
    '''
    try:
        f = open("support/help.txt", "r")
    except FileNotFoundError:
        print("Error: The help file not present!")
        return
    except:
        print("Error opening file")
        return
    print(f.read(), end = '')
    f.close()

