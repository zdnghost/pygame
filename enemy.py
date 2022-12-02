import pygame
from tiles import AnimatedTile
from random import randint
class Enemy(AnimatedTile):
    enemyGroup = pygame.sprite.Group()

    def __init__(self, size, x, y):
        super().__init__(size, x, y,"graphics/enemy/run")
        self.rect.y+=size-self.image.get_size()[1]
        self.speed=randint(3,5)

        #them enemy vao group Sprite
        Enemy.enemyGroup.add(self)
    
    def move(self):
        self.rect.x+=self.speed

    def reverse_image(self):
        if self.speed>0:
            self.image=pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed*=-1

    def update(self, shift):
        self.rect.x+=shift
        self.animated()
        self.move()
        self.reverse_image()
