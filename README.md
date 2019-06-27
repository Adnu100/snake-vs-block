# Snake-vs-Block

A snake vs Block Game written in Python3 using PySDL2 module and sdl2 extensions (sdl2.ext module) for Python3.

## Getting Started
Clone the project into your pc. Open in terminal

***Some parameters like window height, width, frame rate, snake orbs radius etc can be changed by changing the respective parameters in `src/gameinfo.py` ***

***Note that some changes may cause the game to misbehave***

***__All the changes are not flexible__***

### Prerequisites
This game requires Python3 along with the PySDL2 modules installed on your system. To install Python3, enter the command

`sudo apt-get install python3`
`sudo apt-get install python3-pip`

After that, you should install PySDL2 module which is a SDL2 wrapper for Python. Enter the following command in terminal

`pip3 install pysdl2`

Try importing sdl2 library using python3 interpreter to see if it works. If it doesn't work, then set the path to the sdl2 directory in the `PYSDL2_DLL_PATH` variable. It can be done by

```
import os
os.environ["PYSDL2_DLL_PATH"] = "path/to/sdl2/directry"
```

### Setting up the game and running
You may start the game by hitting

`python3 snake`

but instead of typing python3, you can start it by just typing `./snake` by following steps.

Type `which python3` on terminal.
This would give you the path where python3 executable is stored. Use that path instead of the default path in the __src/snake__ file.
The path may differ from pc to pc thus, this customisation is necessary.

Then type following command to run

`./snake`

For help and command line options, Type 

`./snake -h`

`./snake --help`

## License
This project is licensed under GPL-3.0. See LICENSE for details.
