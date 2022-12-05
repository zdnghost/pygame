import pygame
from support import import_folder

player_projectiles = pygame.sprite.Group()

class Projectile(pygame.sprite.Sprite):
    def __init__(self,pos,path,bullet_speed):
        super().__init__()
        self.frames=import_folder(path)
        self.frames_index = 0
        self.bullet_speed = bullet_speed
        self.image = self.frames[self.frames_index]

        self.rect=self.image.get_rect(center = pos)

    def animate(self):
        self.frames_index+=0.15
        if self.frames_index>=len(self.frames):
            self.frames_index=0
        self.image=self.frames[int(self.frames_index)]

    def update(self):
        self.rect.center=(self.rect.center[0]+self.bullet_speed,self.rect.center[1])
        self.animate()