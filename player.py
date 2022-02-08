from turtle import update
import pygame
from pygame.locals import *
from pygame.math import Vector2
import math


class Player(pygame.sprite.Sprite):
    
    sprites = None

    def __init__(self, x, y):
        super().__init__()
        
        if Player.sprites is None:
            Player.sprites = [pygame.image.load('assets/player/player_1.png').convert()]
        
        self.sprites = Player.sprites
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))
        
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        
        self.speed = 400

    def move(self, dt, forwards, sideways):
        speed = self.speed * dt
        if forwards & sideways:
            speed *= math.sqrt(2) / 2

        self.vel = Vector2(sideways * speed, -forwards * speed)
        
    def update_rect(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self):
        self.pos += self.vel
        self.update_rect()
        
        self.image = self.sprites[self.current_sprite]