import pygame
from pygame.math import Vector2
import random
import time
from enemies import Enemy
from constants import *

from abc import ABC, abstractmethod

class Building(ABC, pygame.sprite.Sprite):
    
    sprites = None
    
    def __init__(self, x, y):
        super().__init__()
        
        self.load_sprites()
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x, y))
        
        self.health = 0
        
    @abstractmethod
    def load_sprites(self):
        pass
        
    def update(self):
        if self.health <= 0:
            self.kill()
            

class Barrier(Building):
    
    def __init__(self, x, y):
        super().__init__(x, y)

        self.health = 10
        
    def load_sprites(self):
        if Barrier.sprites is None:
            Barrier.sprites = [pygame.image.load('assets/buildings/barrier.png').convert()]
        
        self.sprites = Barrier.sprites
            
            
class Tower(Building):
    
    def __init__(self, x, y, range, damage):
        super().__init__(x, y)
        
        self.pos = Vector2(x, y)
        
        self.health = 10
        self.damage = damage
        self.range = range
        
        self.cooldown = 1
        self.elapsed_time = 0
        
    def load_sprites(self):
        if Tower.sprites is None:
            Tower.sprites = [pygame.image.load('assets/buildings/ranged_tower.png').convert()]
        
        self.sprites = Tower.sprites

    # for enemies in a certain radius, shoot them
    def shoot(self, enemies: list[Enemy], dt):
        self.elapsed_time += dt
        
        if self.elapsed_time < self.cooldown:
            return None
        
        for enemy in enemies:
            if (enemy.pos - self.pos).length() < self.range:
                self.elapsed_time = 0   
                enemy.health -= self.damage
                
                offset = Vector2(TILE_SIZE/2, TILE_SIZE/2)     
                return [self.pos + offset, enemy.pos + offset]
            
    def draw_range(self, screen):
        pygame.draw.circle(screen, BLACK, (self.pos.x+TILE_SIZE/2, self.pos.y+TILE_SIZE/2), self.range, 1)


class MainBase(Building):

    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.health = 10
        
    def load_sprites(self):
        if MainBase.sprites is None:
            MainBase.sprites = [pygame.image.load('assets/buildings/main_base.png').convert()]
            
        self.sprites = MainBase.sprites