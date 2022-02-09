import pygame
from pygame.math import Vector2
import random
import time
from enemies import Enemy
from copy import deepcopy
from constants import *

class Barrier(pygame.sprite.Sprite):
    
    sprites = None
    
    def __init__(self, x, y):
        super().__init__()
        
        if Barrier.sprites is None:
            Barrier.sprites = [pygame.image.load('assets/buildings/barrier.png').convert()]
        
        self.sprites = Barrier.sprites
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))

        self.health = random.randint(1, 10)

    def kill(self):
        super().kill() 

    def update(self):
        if self.health <= 0:
            self.kill()
            
        self.image = self.sprites[self.current_sprite]


# -----------------------------------------------------------------------------

class RangedTower(pygame.sprite.Sprite):
    
    sprites = None
    
    def __init__(self, x, y, range, damage):
        super().__init__()
        
        if RangedTower.sprites is None:
            RangedTower.sprites = [pygame.image.load('assets/buildings/ranged_tower.png').convert()]
        
        self.sprites = RangedTower.sprites
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))
        
        self.pos = Vector2(x, y)
        
        self.health = random.randint(1, 10)
        self.damage = damage
        self.range = range
        
        self.cooldown = 1
        self.elapsed_time = 0

    def kill(self):
        super().kill() 

    # for enemies in a certain radius, shoot them
    def shoot(self, enemies: list[Enemy], dt):
        self.elapsed_time += dt
        
        if self.elapsed_time < self.cooldown:
            return None
        
        self.elapsed_time = 0
        
        for enemy in enemies:
            if (enemy.pos - self.pos).length() < self.range:
                enemy.health -= self.damage
                offset = Vector2(TILE_SIZE/2, TILE_SIZE/2)
                return [self.pos + offset, enemy.pos + offset]
        
    def update(self):
        if self.health <= 0:
            self.kill()
            
        self.image = self.sprites[self.current_sprite]


class MainBase(pygame.sprite.Sprite):

    sprites = None

    def __init__(self):
        super().__init__()

        if MainBase.sprites is None:
            MainBase.sprites = [pygame.image.load('assets/buildings/main_base.png').convert()]