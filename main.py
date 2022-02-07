import pygame
from timer import Timer
from player import Player
from pygame.locals import *

white = (255,255,255)

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((1280,720), vsync = 0)
    
    clock = Timer()
    
    player = pygame.sprite.GroupSingle()
    player.add(Player(500,500))
    
    running = True
    while running:
        
        # Events ------------------------------------------------- #
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
        keys = pygame.key.get_pressed()
        
        sideways = 0
        forwards = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            sideways -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            sideways += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            forwards += 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            forwards -= 1
        
        # Timer -------------------------------------------------- #
        dt = clock.tick(60)
        fps = clock.get_fps()
        pygame.display.set_caption(f'Running at {fps :.4f}.')
        
        # Background --------------------------------------------- #
        screen.fill(white)
        
        # Render ------------------------------------------------- #
        player.update(dt, forwards, sideways)
        
        player.draw(screen)
        
        # Update ------------------------------------------------- #
        pygame.display.flip()
        
            
if __name__ == '__main__':
    main()
    pygame.quit()
    quit()