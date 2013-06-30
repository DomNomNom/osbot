#!/usr/bin/python

from pyglet import app
import argparse

# our globals
from game.Engine import Engine
# from game.PlayerInput import KeyboardControl, Controller, Replay


# set command line arguments
parser = argparse.ArgumentParser(description='A 2D rocket jumping game. :D')
# parser.add_argument('-e', '--editor', action="store_true", help='Starts the game in editor mode')
parser.add_argument('-l', '--level', help='Loads a level at the start')
# parser.add_argument('-r', '--replay', nargs='+', help='Plays a replay') # TODO: more than 1

# parse command line arguments (note: this can fail and it will exit)
args = parser.parse_args()


# Create global variables
engine = Engine()


levelName = args.level
if not levelName:
  levelName = 'default'

engine.loadLevel(levelName)

# game.globals.gameState.pushState(GameState.Play(playerInputs, levelName))

# engine.addEntity(DebugCross(engine.windowCenter, (1,1,1) ))
# engine.addEntity(DebugCross(engine.mousePos,     (1,0,0) ))


# 3.2.1. GO!
app.run()
