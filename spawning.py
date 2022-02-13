import random 
import time
import pygame

from environment import *
from pygame.locals import *

def spawn_environment(type):

    if self.type == 0:
        tree = Tree(random(screen.width), random(screen.height))
        game_objects['env_objects'].add(tree)
        
    elif self.type == 1:
        rock = Rock(random(screen.width), random(screen.height))
        game_objects['env_objects'].add(rock)
        
    else:
        return None
