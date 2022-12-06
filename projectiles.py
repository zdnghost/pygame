import pygame
from support import import_folder
all_projectiles = pygame.sprite.Group()
player_projectiles = pygame.sprite.Group()

class Projectile(pygame.sprite.Sprite):
    def __init__(self,pos,path,bullet_speed,bullet_range):
        super().__init__()
        self.frames=import_folder(path)
        self.frames_index = 0
        self.bullet_speed = bullet_speed
        self.bullet_range = bullet_range
        self.distance_travelled = 0
        self.image = self.frames[self.frames_index]
        pygame.transform.scale(self.image,(50,50))

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