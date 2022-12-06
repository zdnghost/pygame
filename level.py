import pygame
from particles import ParticleEffect
from support import import_csv_layout,import_cut_graphics
from setting import tile_size,screen_height
from tiles import *
from enemy import *
from decoration import *
from player import Player

import time

import projectiles

class Level:
    def __init__(self,level_data,surface,create_world,current_level):
        #genaral setup
        self.display_surface=surface
        self.world_shift=0
        #player 
        player_layout=import_csv_layout(level_data['player'])
        self.player=pygame.sprite.GroupSingle()
        self.goal=pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        # dust 
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        #terrain setup
        terrain_layout=import_csv_layout(level_data['terrain'])
        self.terrain_sprites=self.create_tile_group(terrain_layout,'terrain')
        
        #grass setup
        grass_layout=import_csv_layout(level_data['grass'])
        self.grass_sprites=self.create_tile_group(grass_layout,'grass')
        
        #creates
        creates_layout=import_csv_layout(level_data['creates'])
        self.creates_sprites=self.create_tile_group(creates_layout,'creates')
        
        #coins
        coins_layout=import_csv_layout(level_data['coins'])
        self.coins_sprites=self.create_tile_group(coins_layout,'coins')
        
        #foreground palms
        fg_palms_layout=import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprites=self.create_tile_group(fg_palms_layout,'fg_palms')
        
        #background palms
        bg_palms_layout=import_csv_layout(level_data['bg_palms'],)
        self.bg_palms_sprites=self.create_tile_group(bg_palms_layout,'bg_palms')
        
        #enemy
        enemy_layout=import_csv_layout(level_data['enemy'],)
        self.enemy_sprites=self.create_tile_group(enemy_layout,'enemy')

        #constraints
        constraints_layout=import_csv_layout(level_data['constraints'],)
        self.constraint_sprite=self.create_tile_group(constraints_layout,'constraints')
        
        #decoration
        self.sky=Sky(5)
        level_width=len(terrain_layout[0])*tile_size
        self.water=Water(screen_height-40,level_width)
        self.clouds=Clouds(400,level_width,20)

        #level select
        self.current_level = current_level
        self.create_world=create_world

        
        self.deathc = 0

    def create_tile_group(self,layout,type):
        spirte_group=pygame.sprite.Group()
         
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val!='-1':
                    x=col_index*tile_size
                    y=row_index*tile_size
                    if type=='terrain':
                        terrains_tile_list=import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surface=terrains_tile_list[int(val)]
                        spirte=StaticTile(tile_size,x,y,tile_surface)
                    
                    if type=='grass':
                        grass_tile_list=import_cut_graphics('graphics/decoration/grass/grass.png')
                        tile_surface=grass_tile_list[int(val)]
                        spirte=StaticTile(tile_size,x,y,tile_surface)
                    
                    if type=='creates':
                        spirte=Crate(tile_size,x,y)

                    if type=='coins':
                        if val=='0' :spirte=Coin(tile_size,x,y,'graphics/coins/gold',Coin.goldType)
                        if val=='1' :spirte=Coin(tile_size,x,y,'graphics/coins/silver',Coin.silverType)
                    if type=='fg_palms':
                        if val=='0':spirte=Palm(tile_size,x,y,'graphics/terrain/palm_small',40)
                        if val=='1':spirte=Palm(tile_size,x,y,'graphics/terrain/palm_large',95)
                    if type=='bg_palms':
                        spirte=Palm(tile_size,x,y,'graphics/terrain/palm_bg',64)
                    if type=='enemy':
                        spirte=Enemy(tile_size,x,y)
                    if type=='constraints':
                        spirte=Tile(tile_size,x,y)

                    spirte_group.add(spirte)

        return spirte_group

    def player_setup(self,layout):
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                x=col_index*tile_size
                y=row_index*tile_size
                if val=='0':
                    sprite=Player((x,y),self.display_surface,self.create_jump_particles)
                    self.player.add(sprite)
                if val=='1':
                    hat_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)

    #=============================================   
    def get_input(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_ESCAPE]):
            self.create_world(self.current_level,'lose')
        elif(keys[pygame.K_RETURN]):
            self.create_world(self.current_level,'win')

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprite,False):
                enemy.reverse()

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.creates_sprites.sprites() + self.fg_palms_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 : 
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.creates_sprites.sprites() + self.fg_palms_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def checkPlayerDeath(self):
        player = self.player.sprite
        hits = pygame.sprite.spritecollide(player , Enemy.enemyGroup, False)
        if(hits):
            print('kill player',self.deathc)
            self.deathc+=1
            #self.playerDie()
        if(player.rect.top>screen_height):
            print('kill player2')
            self.playerDie()
    def playerDie(self):
        self.display_surface.fill("red")
        pygame.display.update()
        time.sleep(2)
        self.create_world(self.current_level,'lose')
        

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)


    def run(self):
        #sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)
        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprite.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        
        #coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)
        #creates
        self.creates_sprites.update(self.world_shift)
        self.creates_sprites.draw(self.display_surface)
        #backgroung palms
        self.bg_palms_sprites.update(self.world_shift)
        self.bg_palms_sprites.draw(self.display_surface)
        #foreground palms
        self.fg_palms_sprites.update(self.world_shift)
        self.fg_palms_sprites.draw(self.display_surface)
        
        #projectiles
        projectiles.player_projectiles.update(self.world_shift)
        projectiles.player_projectiles.draw(self.display_surface)

        #level_input
        self.get_input()

        #player sprites		
        self.player.update()
        self.horizontal_movement_collision()
        
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.checkPlayerDeath()
        
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        #water
        self.water.draw(self.display_surface,self.world_shift)