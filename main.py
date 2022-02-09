# pygame
import pygame
from pygame.locals import *

from timer import Timer
from player import Player
from buildings import Barrier, RangedTower
from enemies import Enemy

from constants import *

import time
import math

from collision import AABB_collision_resolution


def main():
    pygame.init()
    
    screen = pygame.display.set_mode((1280,720), vsync = 0)
    
    clock = Timer()
    
    tiles = {}

    for i in range(0,1280//TILE_SIZE):
        for j in range(0,720//TILE_SIZE):
            tiles[(i,j)] = "Grass"
    
    # Sprite Groups ---------------------------------------------- #
    barriers_list = pygame.sprite.Group()
    towers_list: list[RangedTower] = pygame.sprite.Group()
    buildings_list = pygame.sprite.Group()
    
    enemies_list = pygame.sprite.Group()
    player_sprite = pygame.sprite.GroupSingle()
    
    projectiles_list = []
    
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
                    
                if event.key in SPAWN_KEYS:
                    pos = pygame.mouse.get_pos()
                        
                    i = pos[0] // TILE_SIZE
                    j = pos[1] // TILE_SIZE
                    
                    x = i * TILE_SIZE
                    y = j * TILE_SIZE
                    
                    if event.key == pygame.K_1:
                        enemy = Enemy(pos[0] - TILE_SIZE/2, pos[1] - TILE_SIZE/2)
                        enemies_list.add(enemy)
                
                    if event.key == pygame.K_2:
                        if tiles[(i,j)] == "Grass":
                            barrier = Barrier(x, y)
                            barriers_list.add(barrier)
                            buildings_list.add(barrier)
                        
                            tiles[(i,j)] = "Barrier"
                    
                    if event.key == pygame.K_3:
                        if tiles[(i,j)] == "Grass":
                            tower = RangedTower(x, y, 500, 1)
                            towers_list.add(tower)
                            buildings_list.add(tower)

                            tiles[(i,j)] = "RangedTower"
                        
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
            
        # Movement/Logic ------------------------------------------------ #
        for enemy in enemies_list:
            enemy.move(dt, player.pos)
        player.move(dt, forwards, sideways)
        
        for tower in towers_list:
            info = tower.shoot(enemies_list, dt)
            if info != None:
                projectiles_list.append(info + [1])
        
        # Update ------------------------------------------------- #
        barriers_list.update()
        towers_list.update()
        enemies_list.update()
        player.update()
        
        for info in projectiles_list:
            info[2] -= dt
            if info[2] <= 0:
                projectiles_list.remove(info)
        
        # player-building collision
        collided = pygame.sprite.spritecollide(player, buildings_list, False)
        # sort from nearest to prevent edge clipping
        collided.sort(key = lambda sprite: math.dist((sprite.rect.x, sprite.rect.y), (player.pos.x, player.pos.y)))
        # collision resolution
        for building in collided:
            AABB_collision_resolution(player, building)
            
        # enemy-building collision
        collided_dict = pygame.sprite.groupcollide(enemies_list, buildings_list, False, False)
        for enemy, collided in collided_dict.items():
            collided.sort(key = lambda sprite: math.dist((sprite.rect.x, sprite.rect.y), (enemy.pos.x, enemy.pos.y)))
            for building in collided:
                AABB_collision_resolution(enemy, building)
        
        # Render ------------------------------------------------- #
        screen.fill((200, 200, 200))
        
        barriers_list.draw(screen)
        towers_list.draw(screen)
        enemies_list.draw(screen)
        player_sprite.draw(screen)
        
        for info in projectiles_list:
            pygame.draw.line(screen, (255, 0, 0), info[0], info[1], 2)
        
        pygame.display.flip()
            
if __name__ == '__main__':
    main()
    pygame.quit()
    quit()