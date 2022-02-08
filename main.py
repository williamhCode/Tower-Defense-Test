# pygame
from tkinter import LEFT, RIGHT
import pygame
from pygame.locals import *

from timer import Timer
from player import Player

import time
import math

from collision import AABB_collision_resolution

WHITE = (255,255,255)
TILE_SIZE = 32

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((1280,720), vsync = 0)
    
    # imports for objects with image caching (has to be after pygame.init() and pygame.display.set_mode())
    from buildings import Barrier
    from enemies import Enemy
    
    clock = Timer()
    
    buildings = {}
    
    # Sprite Groups ---------------------------------------------- #
    buildings_sprites = pygame.sprite.Group()
    enemies_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.GroupSingle()
    
    # Player ----------------------------------------------------- #
    player = Player(500,500)
    player_sprite.add(player)
    
    running = True

    while running:
        
        # Timer -------------------------------------------------- #
        dt = clock.tick(60)
        fps = clock.get_fps()
        pygame.display.set_caption(f'Running at {fps :.4f}.')

        # Events ------------------------------------------------- #
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
            
                if event.button == 1:
                    i = pos[0] // TILE_SIZE
                    j = pos[1] // TILE_SIZE
                    
                    x = i * TILE_SIZE
                    y = j * TILE_SIZE
                    
                    barrier = Barrier(x, y)
                    buildings[(i,j)] = barrier
                    buildings_sprites.add(barrier)
                    
                if event.button == 3:
                    enemy = Enemy(pos[0] - TILE_SIZE/2, pos[1] - TILE_SIZE/2)
                    enemies_sprites.add(enemy)
                    
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
            
        # Movement ------------------------------------------------ #
        for enemy in enemies_sprites:
            enemy.move(dt, player.pos)
        player.move(dt, forwards, sideways)
        
        # Update ------------------------------------------------- #
        enemies_sprites.update()
        player.update()
        
        # player-building collision
        collided = pygame.sprite.spritecollide(player, buildings_sprites, False)
        # sort from nearest to prevent edge clipping
        collided.sort(key = lambda sprite: math.dist((sprite.rect.x, sprite.rect.y), (player.rect.x, player.rect.y)))
        # collision resolution
        for building in collided:
            AABB_collision_resolution(player, building)
            
        # enemy-building collision
        collided_dict = pygame.sprite.groupcollide(enemies_sprites, buildings_sprites, False, False)
        for enemy, collided in collided_dict.items():
            for building in collided:
                AABB_collision_resolution(enemy, building)
        
        # Render ------------------------------------------------- #
        screen.fill((200, 200, 200))
        
        buildings_sprites.draw(screen)
        enemies_sprites.draw(screen)
        player_sprite.draw(screen)
        
        pygame.display.flip()
            
if __name__ == '__main__':
    main()
    pygame.quit()
    quit()