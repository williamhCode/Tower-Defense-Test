import pygame 
from pygame.math import Vector2

class Enemy(pygame.sprite.Sprite):
    
    sprites = None
    
    def __init__(self, x, y):
        super().__init__()
        
        if Enemy.sprites is None:
            Enemy.sprites = [pygame.image.load('assets/enemies/enemy_1.png').convert()]
            
        self.sprites = Enemy.sprites

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))

        self.pos = Vector2(x, y)
        self.speed = 100
        
        self.health = 5
    
    def move(self, dt, target_pos):
        dir = (target_pos - self.pos).normalize()
        self.vel = dir * self.speed * dt
        
    def update_rect(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self):
        self.pos += self.vel
        self.update_rect()
        
        self.image = self.sprites[self.current_sprite]
