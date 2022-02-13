import pygame

from abc import ABC, abstractmethod

class EnvObject(ABC, pygame.sprite.Sprite):
    
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
            
            
class Rock(EnvObject):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.health = 10
        
    def load_sprites(self):
        if Rock.sprites is None:
            Rock.sprites = [pygame.image.load('assets/environment/rock.png').convert_alpha()]
        
        self.sprites = Rock.sprites
        
        
class Tree(EnvObject):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.health = 10
        
    def load_sprites(self):
        if Tree.sprites is None:
            Tree.sprites = [pygame.image.load('assets/environment/tree.png').convert_alpha()]
        
        Tree.sprites = Tree.sprites
        
    