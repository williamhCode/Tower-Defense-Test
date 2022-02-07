import pygame
from pygame.locals import *
import math

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('assets/player/player_1.png').convert_alpha())
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))
        
        self.speed = 400

    def move(self, dt, forwards, sideways):
        speed = self.speed * dt
        if forwards & sideways:
            speed *= math.sqrt(2) / 2

        self.rect.y -= forwards * speed
        self.rect.x += sideways * speed

    def update(self, dt, forwards, sideways):
        self.move(dt, forwards, sideways)
        
        self.image = self.sprites[self.current_sprite]