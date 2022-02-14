from numpy import angle
import pygame
from pygame.locals import *
from pygame.math import Vector2
import math
from environment import Rock, Tree

from inventory import Inventory

class Player(pygame.sprite.Sprite):
    
    sprites = None

    def __init__(self, x, y):
        super().__init__()
        
        if Player.sprites is None:
            Player.sprites = [pygame.image.load('assets/player/player_1.png').convert()]
        
        self.sprites = Player.sprites
        
        self.axe_img = pygame.image.load('assets/player/axe.png').convert()
        self.axe_img = pygame.transform.scale2x(self.axe_img)
        self.axe_offset = Vector2(0, -self.axe_img.get_height()/2)
        
        self.rot_axe_img: pygame.surface.Surface = None
        self.axe_rect: pygame.rect.Rect = None
        
        self.axe_pos = Vector2(0, 0)
        self.axe_dir = Vector2(0, 0)
        self.axe_radius = 25
        
        self.cooldown = 0.4
        self.elapsed_time = 1
        self.hit_ang = 0
        
        self.damage = 1
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))
        
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        
        self.speed = 200
        
        self.inventory = Inventory()

    def move(self, dt, forwards, sideways):
        speed = self.speed * dt
        if forwards & sideways:
            speed *= math.sqrt(2) / 2

        self.vel = Vector2(sideways * speed, -forwards * speed)
        
    def hit(self, env_objects: pygame.sprite.Group()):
        
        if self.elapsed_time < self.cooldown:
            return
        
        self.elapsed_time = 0
        self.hit_ang = 60
        self.update_axe()
        
        for sprite in env_objects:
            if sprite.rect.colliderect(self.axe_rect):
                if sprite.being_hit(self.damage):
                    if isinstance(sprite, Rock):
                        self.inventory.add_stone()
                    elif isinstance(sprite, Tree):
                        self.inventory.add_wood()
                return
        
    def set_axe_dir(self, mouse_pos):
        mouse_pos = Vector2(mouse_pos)
        self.axe_dir = mouse_pos - (self.pos + (16, 0))
        self.axe_dir.normalize_ip()
        
    def update_axe(self):
        self.axe_pos = self.pos + (16, 16) + self.axe_dir * self.axe_radius
        dir = self.axe_dir.dot(Vector2(1, 0))
        angle = self.axe_dir.angle_to(Vector2(0, 0)) - self.hit_ang if dir > 0 else self.axe_dir.angle_to(Vector2(0, 0)) + 180 + self.hit_ang
        self.rot_axe_img, self.axe_rect = rotate(self.axe_img, angle, self.axe_pos, self.axe_offset)
        
    def update_rect(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    def update(self, dt):
        self.pos += self.vel
        self.update_rect()
        self.update_axe()
        
        self.elapsed_time += dt
        if self.elapsed_time < self.cooldown:
            self.hit_ang = 60 * (1 - self.elapsed_time / self.cooldown)
        
        self.image = self.sprites[self.current_sprite]
        
    def draw_axe(self, screen):
        screen.blit(self.rot_axe_img, self.axe_rect)
        
def rotate(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotozoom(surface, angle, 1)
    rotated_offset = offset.rotate(-angle)
    rect = rotated_image.get_rect(center= pivot+rotated_offset)
    return rotated_image, rect