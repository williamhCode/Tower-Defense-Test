import pygame

class Barrier(pygame.sprite.Sprite):
    
    sprites = [pygame.image.load('assets/buildings/barrier.png').convert(),
               ]
    
    def __init__(self, x, y):
        super().__init__()
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))
        self.health = 10
        
    # def update(self):
    #     self.image = self.sprites[self.current_sprite]