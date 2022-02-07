from collision import AABB_collision_resolution
import pygame
from timer import Timer
from player import Player
from pygame.locals import *
import time
import math

WHITE = (255,255,255)
TILE_SIZE = 32

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((1280,720), vsync = 0)
    
    # imports for objects with image caching (has to be after pygame.init() and pygame.display.set_mode())
    from buildings import Barrier
    
    clock = Timer()
    
    buildings = {}
    buildings_sprites = pygame.sprite.Group()
    
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
                    
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                i = pos[0] // TILE_SIZE
                j = pos[1] // TILE_SIZE
                barrier = Barrier(i*TILE_SIZE, j*TILE_SIZE)
                
                buildings[(i,j)] = barrier
                buildings_sprites.add(barrier)
                    
        keys = pygame.key.get_pressed()
        
        forwards = 0
        sideways = 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            forwards += 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            forwards -= 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            sideways -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            sideways += 1
        
        # Timer -------------------------------------------------- #
        dt = clock.tick(60)
        fps = clock.get_fps()
        pygame.display.set_caption(f'Running at {fps :.4f}.')
        
        # Update ------------------------------------------------- #
        player.update(dt, forwards, sideways)
        
        # player-building collision
        p_sprite = player.sprite
        collided = pygame.sprite.spritecollide(p_sprite, buildings_sprites, False)
        # sort from nearest to prevent edge clipping
        p_pos = (p_sprite.rect.x, p_sprite.rect.y)
        collided.sort(key = lambda sprite: math.dist((sprite.rect.x, sprite.rect.y), p_pos))
        # collision resolution
        for building in collided:
            AABB_collision_resolution(building, player.sprite)
        
        # Render ------------------------------------------------- #
        screen.fill(WHITE)
        
        player.draw(screen)
        buildings_sprites.draw(screen)
        
        # Update ------------------------------------------------- #
        pygame.display.flip()
        
            
if __name__ == '__main__':
    main()
    pygame.quit()
    quit()