import pygame 

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('assets/enemies/enemy_1.png').convert())

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (x,y))

        self.health = 5
        self.speed = 300
    
    def move(self, dt, x, tx, y, ty):
        speed = self.speed * dt
        if x > tx:
            self.rect.x -= speed
        elif x < tx:
            self.rect.x += speed
        if y > ty:
            self.rect.y -= speed
        elif y < ty:
            self.rect.y += speed
        #if self.rect.x == tx and self.rect.y == ty:
            #self.health -= 1
            #if self.health == 0:
                #self.kill()

    def update(self, dt, x, y):
        self.move(dt, x, y)
        self.image = self.sprites[self.current_sprite]
