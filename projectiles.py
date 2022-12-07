import pygame
from support import import_folder
all_projectiles = pygame.sprite.Group()
player_projectiles = pygame.sprite.Group()

class Projectile(pygame.sprite.Sprite):
    def __init__(self,pos,path,direction,speed,size,range):
        super().__init__()
        self.frames=import_folder(path)
        for index,frame in enumerate(self.frames):
            self.frames[index]=pygame.transform.scale(frame,size)

        self.frames_index = 0
        
        if(direction=='right'):
            self.bullet_speed = speed
        else:
            self.bullet_speed = -speed
            for index,frame in enumerate(self.frames):
                self.frames[index]=pygame.transform.rotate(frame,180)

        self.bullet_range = range
        self.distance_travelled = 0
        self.image = self.frames[self.frames_index]

        self.rect=self.image.get_rect(center = pos)

        all_projectiles.add(self)

    def animate(self):
        self.frames_index+=0.15
        if self.frames_index>=len(self.frames):
            self.frames_index=0
        self.image=self.frames[int(self.frames_index)]

    def update(self,shift):
        self.rect.center=(self.rect.center[0]+self.bullet_speed,self.rect.center[1])
        self.distance_travelled+=self.bullet_speed
        self.animate()
        if(self.distance_travelled>self.bullet_range):
            self.kill()

        self.rect.x+=shift