import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y
        self.sprites.append(pygame.image.load('assets/player/player_1.png').convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))
        
        self.speed = 500

    def move(self, dt, forwards, sideways):
        self.y -= forwards * self.speed * dt
        self.x += sideways * self.speed * dt

    def update(self, dt, forwards, sideways):
        self.move(dt, forwards, sideways)
        
        self.rect = Rect(self.x, self.y, self.rect.width, self.rect.height)
        
        self.image = self.sprites[self.current_sprite]