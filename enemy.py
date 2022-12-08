import pygame
from support import *
from tiles import AnimatedTile
from random import randint # gọi hàm random 
class Enemy(AnimatedTile):

    def __init__(self, size, x, y,display_surface):
        super().__init__(size, x, y,"graphics/enemy/run")
        self.rect.y+=size-self.image.get_size()[1]
        self.speed=randint(3,5)
        # tạo ngẫu nhiên tốc độ của quái
        self.import_hit_effect()

        self.is_hit=False
        self.display_surface = display_surface
        self.hit_effect_frames_index = 0
        self.hit_effect_animation_speed = 0.15
        self.death_time = 0
        self.clock = pygame.time.Clock()

    
    def move(self): # hàm di chuyển quái
        self.rect.x+=self.speed

    def import_hit_effect(self):
        self.hit_effect_frames=import_folder('graphics/enemy/explosion')
        for index,frame in enumerate(self.hit_effect_frames):
            self.hit_effect_frames[index]=pygame.transform.scale(frame,(70,70))

    def run_hit_effect(self):
        if self.is_hit == True:
            self.hit_effect_frames_index+=self.hit_effect_animation_speed
            if self.hit_effect_frames_index>=len(self.hit_effect_frames):
                self.hit_effect_frames_index=0
            self.hit_effect_image=self.hit_effect_frames[int(self.hit_effect_frames_index)]
            self.display_surface.blit(self.hit_effect_image,self.rect.topleft+pygame.math.Vector2(-25,-10))

    def reverse_image(self):# đảo ngược hoạt ảnh khi di chuyển ngược lại
        if self.speed>0:
            self.image=pygame.transform.flip(self.image,True,False)

    def reverse(self): # di chuyển ngược lại
        self.speed*=-1

    def checkIfDeath(self):
        if self.is_hit==True:
            self.death_time += self.clock.tick()
            if(self.death_time>300):
                self.kill()
        else:
            self.clock.tick()

        
    # cập nhập lại vị trí và hoạt ảnh trong game
    def update(self, shift):  
        self.rect.x+=shift
        
        if self.is_hit == False:
            self.animated()
            self.move()
            self.reverse_image()
        self.run_hit_effect()
        self.checkIfDeath()