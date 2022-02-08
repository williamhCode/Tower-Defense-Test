import pygame
from pygame.math import Vector2

import random
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

        self.health = random.randint(1,10)

    def kill(self):
        super().kill() 

    def update(self):
        if self.health <= 0:
            self.kill()
            
        self.image = self.sprites[self.current_sprite]