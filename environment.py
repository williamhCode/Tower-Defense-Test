import pygame
from pygame.math import Vector2

from abc import ABC, abstractmethod

class EnvObject(ABC, pygame.sprite.Sprite):
    
    sprites = None
    
    def __init__(self, x, y):
        super().__init__()
        
        self.load_sprites()
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x, y))
        
        self.pos = Vector2(x, y)
        
        self.health = 0
        
        self.damaged = False
        self.elapsed_time = 0
        self.cooldown = 0.3
        
    def damage(self, amount):
        self.health -= amount
        self.damaged = True
        self.elapsed_time = 0
        self.current_sprite = 1
        return self.health <= 0
        
    @abstractmethod
    def load_sprites(self):
        pass
        
    def update(self, dt):
        if self.health <= 0:
            self.kill()
            
        if self.damaged:
            self.elapsed_time += dt
            if self.elapsed_time > self.cooldown:
                self.damaged = False
                self.current_sprite = 0
            
        self.image = self.sprites[self.current_sprite]
            
            
class Rock(EnvObject):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.health = 5
        
    def load_sprites(self):
        if Rock.sprites is None:
            Rock.sprites = [pygame.image.load('assets/environment/rock.png').convert_alpha()]
            # blit red transparent rectangle onto rock
            rock_2 = Rock.sprites[0].copy()
            surf = pygame.Surface(rock_2.get_size())
            surf.set_alpha(128)
            surf.fill((255,0,0))
            rock_2.blit(surf, (0,0))
            Rock.sprites.append(rock_2)
        
        self.sprites = Rock.sprites
        
        
class Tree(EnvObject):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.health = 3
        
    def load_sprites(self):
        if Tree.sprites is None:
            Tree.sprites = [pygame.image.load('assets/environment/tree.png').convert_alpha()]
            
            tree_2 = Tree.sprites[0].copy()
            surf = pygame.Surface(tree_2.get_size())
            surf.set_alpha(128)
            surf.fill((255,0,0))
            tree_2.blit(surf, (0,0))
            Tree.sprites.append(tree_2)
        
        Tree.sprites = Tree.sprites
        
    