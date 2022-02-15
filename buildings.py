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
        
        self.pos = Vector2(x, y)
        
        self.health = 0
        
        self.is_damaged = False
        self.elapsed_time = 0
        self.cooldown = 0.3
        
    def damaged(self, amount):
        self.health -= amount
        self.is_damaged = True
        self.elapsed_time = 0
        self.current_sprite = 1
        return self.health <= 0
        
    @abstractmethod
    def load_sprites(self):
        pass
        
    def update(self, dt):
        if self.health <= 0:
            self.kill()
            
        if self.is_damaged:
            self.elapsed_time += dt
            if self.elapsed_time > self.cooldown:
                self.is_damaged = False
                self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]

class Barrier(Building):
    
    def __init__(self, x, y):
        super().__init__(x, y)

        self.health = 5
        
    def load_sprites(self):
        if Barrier.sprites is None:
            Barrier.sprites = [pygame.image.load('assets/buildings/barrier.png').convert()]
            
            barrier_2 = Barrier.sprites[0].copy()
            surf = pygame.Surface(barrier_2.get_size())
            surf.set_alpha(128)
            surf.fill((255,0,0))
            barrier_2.blit(surf, (0,0))
            Barrier.sprites.append(barrier_2)
        
        self.sprites = Barrier.sprites

            
class Tower(Building):
    
    def __init__(self, x, y, range, damage):
        super().__init__(x, y)
        
        self.health = 10
        self.damage = damage
        self.range = range
        
        self.attack_cooldown = 1
        self.attack_elapsed_time = 0
        
    def load_sprites(self):
        if Tower.sprites is None:
            Tower.sprites = [pygame.image.load('assets/buildings/ranged_tower.png').convert()]
            
            tower_2 = Tower.sprites[0].copy()
            surf = pygame.Surface(tower_2.get_size())
            surf.set_alpha(128)
            surf.fill((255,0,0))
            tower_2.blit(surf, (0,0))
            Tower.sprites.append(tower_2)
        
        self.sprites = Tower.sprites

    # for enemies in a certain radius, shoot them
    def shoot(self, enemies: list[Enemy]):
        if self.attack_elapsed_time < self.attack_cooldown:
            return None
        
        for enemy in enemies:
            if (enemy.pos - self.pos).length() < self.range:
                self.attack_elapsed_time = 0   
                enemy.health -= self.damage
                
                offset = Vector2(TILE_SIZE/2, TILE_SIZE/2)     
                return [self.pos + offset, enemy.pos + offset]
            
    def draw_range(self, screen):
        pygame.draw.circle(screen, BLACK, (self.pos.x+TILE_SIZE/2, self.pos.y+TILE_SIZE/2), self.range, 1)
        
    def update(self, dt):
        self.attack_elapsed_time += dt
        super().update(dt)


class MainBase(Building):

    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.health = 20
        
    def load_sprites(self):
        if MainBase.sprites is None:
            MainBase.sprites = [pygame.image.load('assets/buildings/main_base.png').convert()]
            
            main_base_2 = MainBase.sprites[0].copy()
            surf = pygame.Surface(main_base_2.get_size())
            surf.set_alpha(128)
            surf.fill((255,0,0))
            main_base_2.blit(surf, (0,0))
            MainBase.sprites.append(main_base_2)
            
        self.sprites = MainBase.sprites
