import pygame 
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):
    
    sprites = None
    
    def __init__(self, x, y):
        super().__init__()
        
        if Enemy.sprites is None:
            Enemy.sprites = [pygame.image.load('assets/enemies/enemy_1.png').convert()]
            
            enemy_2 = Enemy.sprites[0].copy()
            surf = pygame.Surface(enemy_2.get_size())
            surf.set_alpha(128)
            surf.fill((255,0,0))
            enemy_2.blit(surf, (0,0))
            Enemy.sprites.append(enemy_2)
            
        self.sprites = Enemy.sprites

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))

        self.pos = Vector2(x, y)
        self.speed = 60
        
        self.health = 6
        
        self.damaged = False
        self.elapsed_time = 0
        self.cooldown = 0.3
        
    def damage(self, amount):
        self.health -= amount
        self.damaged = True
        self.elapsed_time = 0
        self.current_sprite = 1
        return self.health <= 0
    
    def move(self, dt, target_pos):
        dir = (target_pos - self.pos).normalize()
        self.vel = dir * self.speed * dt
        
    def update_rect(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self, dt):
        self.pos += self.vel
        self.update_rect()
        
        if self.health <= 0:
            self.kill()
            
        if self.damaged:
            self.elapsed_time += dt
            if self.elapsed_time > self.cooldown:
                self.damaged = False
                self.current_sprite = 0
        
        self.image = self.sprites[self.current_sprite]
