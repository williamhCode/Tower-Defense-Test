from random import *
import time
from constants import *

from environment import *
from pygame.locals import *

def spawn_environment(kind, game_objects):

    if kind == 0:
        tree = Tree(randint(0, WIDTH), randint(0, HEIGHT))
        game_objects['env_objects'].add(tree)
        
    elif kind == 1:
        rock = Rock(randint(0, WIDTH), randint(0, HEIGHT))
        game_objects['env_objects'].add(rock)
        
    else:
        return None
