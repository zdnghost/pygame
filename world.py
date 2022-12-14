import pygame
from game_data import levels
from support import *

# thể hiện cho các khung level thể hiện trong menu dòng
class levelNode (pygame.sprite.Sprite): 
    def __init__(self,pos,status,path):
        super().__init__()
        self.frames=import_folder(path)
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.status = status

        self.rect=self.image.get_rect(center = pos)

    #hàm chuyển động cho các khung level
    def animate(self):
        self.frames_index+=0.15
        if self.frames_index>=len(self.frames):
            self.frames_index=0
        self.image=self.frames[int(self.frames_index)]

    def update(self):
        if(self.status=='available'):
            self.animate()
        else:
            tint_surf =  self.image.copy()
            tint_surf.fill(pygame.Color(10,10,10,100),None,pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf,(0,0))
            
# lớp tạo cái icon chọn dòng
class PlayerIcon (pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(r'graphics\character\Untitled.png')
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.center=self.pos

#lớp thể hiện khung cửa sổ chứa tất cả khung và icon
class World:
    def __init__(self,start_level,max_level,surface,create_level):
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level=create_level

        # di chuyển icon giữa các khung menu khác nhau
        self.not_moving = True
        self.move_direction = pygame.math.Vector2(0,0)
        self.move_speed=14

        #create node
        self.setup_nodes() # tạo 4 cái hình node đại diện cho màn chơi
        self.setup_playerIcon() # tạo icon tượng trưng để chọn dòng

        self.background_image = pygame.image.load('graphics/overworld/sea_background.jpg')
    
    def setup_nodes(self): # thể hiện node
        self.nodes = pygame.sprite.Group()
        
        for index,node_data in enumerate(levels.values()):
            if(index<=self.max_level):
                node_sprites = levelNode(node_data['node_pos'],'available',node_data['node_graphics'])
                self.nodes.add(node_sprites)# thể hiện các màn chơi đã mở khóa
            else:
                node_sprites = levelNode(node_data['node_pos'],'locked',node_data['node_graphics'])
                self.nodes.add(node_sprites)# thể hiện các màn chơi chưa mở khóa
            
    def setup_playerIcon(self): # setup icon
        self.icon = pygame.sprite.GroupSingle()
        player = PlayerIcon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(player)

    def draw_paths(self): # đường thẳng nối các khung
        points = [node['node_pos'] for index,node in enumerate(levels.values()) if index<=self.max_level]
        pygame.draw.lines(self.display_surface,'red',False,points,4)

    def get_input(self): # chọn dòng chơi
        if(self.not_moving):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d] and self.current_level<self.max_level:
                self.not_moving=False
                self.move_direction = self.get_movement_data('right')
                self.current_level+=1
            elif keys[pygame.K_a] and self.current_level>0:
                self.not_moving=False
                self.move_direction = self.get_movement_data('left')
                self.current_level-=1
            if keys[pygame.K_SPACE]:    # nhấn space để chọn dòng chơi
                self.create_level(self.current_level)
    
    def get_movement_data(self,direction):# di chuyển icon giữa các khung
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if(direction=='left'):
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)
        elif(direction=='right'):
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)

        return (end-start).normalize()

    def update_icon_pos(self):
        if(not self.not_moving):
            self.icon.sprite.prev_pos = self.icon.sprite.pos
            self.icon.sprite.pos+=self.move_direction*self.move_speed
            self.icon.sprite.update()
            if(self.icon.sprite.rect.center==self.nodes.sprites()[self.current_level].rect.center):
                self.not_moving=True
            elif(self.icon.sprite.prev_pos):
                icon_pos = self.icon.sprite.pos
                node_pos = self.nodes.sprites()[self.current_level].rect.center
                
                if(self.move_direction[0]>0):
                    if(abs(icon_pos[0])>abs(node_pos[0])):
                            self.not_moving=True
                            self.icon.sprite.pos=node_pos
                            self.icon.sprite.update()
                
                if(self.move_direction[0]<0):
                    if(abs(icon_pos[0])<abs(node_pos[0])):
                            self.not_moving=True
                            self.icon.sprite.pos=node_pos
                            self.icon.sprite.update()

    def run(self):
        self.display_surface.blit(self.background_image,self.background_image.get_rect(topleft=(0,0)))
        self.get_input()
        self.draw_paths()
        self.nodes.update()

        self.nodes.draw(self.display_surface)

        self.update_icon_pos()
        self.icon.draw(self.display_surface)
        