from random import *
import time
import pygame
from constants import *

screen = pygame.display.set_mode((1280, 720), vsync=0)


from environment import *
from pygame.locals import *

def spawn_environment(kine, game_objects):

    if kine == 0:
        tree = Tree(randint(0, WIDTH), randint(0, HEIGHT))
        game_objects['env_objects'].add(tree)
        
    elif kine == 1:
        rock = Rock(randint(0, WIDTH), randint(0, HEIGHT))
        game_objects['env_objects'].add(rock)
        
    else:
        return None
