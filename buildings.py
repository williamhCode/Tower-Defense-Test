import pygame

class Barrier(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('assets/buildings/barrier.png').convert())
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))
    
        self.health = 10
        
    # def update(self):
    #     self.image = self.sprites[self.current_sprite]