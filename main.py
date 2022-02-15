# pygame
import pygame
from pygame.locals import *
from environment import Rock, Tree

from timer import Timer
from player import Player
from buildings import Barrier, MainBase, Tower
from enemies import Enemy
from constants import *
from spawning import *
import time
import math
import random


from collision import AABB_collision_resolution


class GroupWrapper:
    
    def __init__(self, *sprite_groups: pygame.sprite.Group):
        self.group = pygame.sprite.Group()
        self.sprite_groups = [self.group, *sprite_groups]
        
        self.update_sprites()
        
    def add(self, sprite):
        self.group.add(sprite)
        
    def __iter__(self):
        return iter(self.sprites)
        
    def update_sprites(self):
        sprites = []
        for group in self.sprite_groups:
            sprites += group.sprites()
        self.sprites = sprites
    
    def update(self, dt):
        for group in self.sprite_groups:
            group.update(dt)
            
    def draw(self, surface):
        for group in self.sprite_groups:
            group.draw(surface)
            

def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 20)
    
    screen = pygame.display.set_mode((1280, 720), vsync=0)
    
    clock = Timer()
    
    tiles = {}

    for i in range(0, 1280//TILE_SIZE+1):
        for j in range(0, 720//TILE_SIZE+1):
            tiles[(i,j)] = "Grass"
    
    # Init Objects ----------------------------------------------------- #
    game_objects_keys = ('barriers', 'towers', 'env_objects', 'enemies')
    game_objects = {key: pygame.sprite.Group() for key in game_objects_keys}
    game_objects['buildings'] = GroupWrapper(game_objects['barriers'], game_objects['towers'])
    game_objects['player'] = pygame.sprite.GroupSingle()
    
    static_groups = (game_objects['env_objects'], game_objects['buildings'])
    dynamic_groups = (game_objects['enemies'], game_objects['player'])
    
    # initial spawn
    for _ in range(30):
        spawn_environment(randint(0, 2), game_objects)
    
    projectiles_list = []
    
    debug = False
    
    player = Player(500,500)
    game_objects['player'].add(player)
    
    base = MainBase(600, 300)
    game_objects['buildings'].add(base)
    
    running = True

    while running:
        
        # Timer -------------------------------------------------- #
        dt = clock.tick(60)
        fps = clock.get_fps()
        pygame.display.set_caption(f'Running at {fps :.4f}.')

        # Events ------------------------------------------------- #
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    player.hit(game_objects)
                
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                if event.key == pygame.K_f:
                    debug = not debug
                    
                if event.key in SPAWN_KEYS:
                        
                    i = pos[0] // TILE_SIZE
                    j = pos[1] // TILE_SIZE
                    
                    x = i * TILE_SIZE
                    y = j * TILE_SIZE
                    
                    if event.key == pygame.K_1:
                        enemy = Enemy(pos[0] - TILE_SIZE/2, pos[1] - TILE_SIZE/2)
                        game_objects['enemies'].add(enemy)
                
                    if event.key == pygame.K_2:
                        if tiles[(i,j)] == "Grass":
                            barrier = Barrier(x, y)
                            game_objects['barriers'].add(barrier)
                            player.inventory.wood -= 3
                        
                            tiles[(i,j)] = barrier
                    
                    if event.key == pygame.K_3:
                        if tiles[(i,j)] == "Grass":
                            tower = Tower(x, y, 150, 1)
                            game_objects['towers'].add(tower)
                            player.inventory.wood -= 2
                            player.inventory.stone -= 2
                            
                            tiles[(i,j)] = tower
                            
                    if event.key == pygame.K_4:
                        rock = Rock(*pos)
                        game_objects['env_objects'].add(rock)
                        
                    if event.key == pygame.K_5:
                        tree = Tree(*pos)
                        game_objects['env_objects'].add(tree)

                    if event.key == pygame.K_6:
                        spawn_environment(randint(0, 1), game_objects)

                    if event.key == pygame.K_e:
                        curr = tiles[(i,j)]
                        if isinstance(curr, Barrier | Tower):
                            curr.kill()
                            tiles[(i,j)] = "Grass"

        game_objects['buildings'].update_sprites()
                        
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
        for enemy in game_objects['enemies']:
            enemy.move(dt, base.pos + (base.rect.width/4, base.rect.height/4))
        player.move(dt, forwards, sideways)
        player.set_axe_dir(pos)
        
        for tower in game_objects['towers']:
            info = tower.shoot(game_objects['enemies'])
            if info != None:
                projectiles_list.append(info + [0.2])
        
        # Update ------------------------------------------------- # 
        for group in game_objects.values():
            group.update(dt)
        
        for info in projectiles_list:
            info[2] -= dt
            if info[2] <= 0:
                projectiles_list.remove(info)
        
        # collision resolution
        for dynamic_group in dynamic_groups:
            
            is_enemies = False
            if dynamic_group is game_objects['enemies']:
                is_enemies = True
            
            for static_group in static_groups:
                
                collided_dict = pygame.sprite.groupcollide(dynamic_group, static_group, False, False)
                
                for dynamic, collided in collided_dict.items():
                    collided.sort(key = lambda sprite: math.dist((sprite.rect.x, sprite.rect.y), (dynamic.pos.x, dynamic.pos.y)))
                    
                    for static in collided:
                        if AABB_collision_resolution(dynamic, static) and is_enemies:
                            dynamic.attack(static)
                            # pass
                
        # Render ------------------------------------------------- #
        screen.fill((200, 200, 200))
        
        for group in game_objects.values():
            group.draw(screen)
        
        for info in projectiles_list:
            pygame.draw.line(screen, (255, 0, 0), info[0], info[1], 2)
            
        player.draw_axe(screen)
            
        if debug:
            for tower in game_objects['towers']:
                tower.draw_range(screen)
                
        inv = player.inventory
        text = f'Stone: {inv.stone}, Wood: {inv.wood}, Gold: {inv.gold}'
        text_surf = font.render(text, False, (0, 0, 0))
        screen.blit(text_surf, (10, 0))
        
        text_surf = font.render(f'Base HP: {base.health}', False, (0, 0, 0))
        screen.blit(text_surf, (10, 30))
        
        pygame.display.flip()
            
if __name__ == '__main__':
    main()
    pygame.quit()
    quit()