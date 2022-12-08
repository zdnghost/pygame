import pygame
from tiles import AnimatedTile
from random import randint # gọi hàm random 
class Enemy(AnimatedTile):

    def __init__(self, size, x, y):
        super().__init__(size, x, y,"graphics/enemy/run")
        self.rect.y+=size-self.image.get_size()[1]
        self.speed=randint(3,5)
        # tạo ngẫu nhiên tốc độ của quái
    
    def move(self): # hàm di chuyển quái
        self.rect.x+=self.speed

    def reverse_image(self):# đảo ngược hoạt ảnh khi di chuyển ngược lại
        if self.speed>0:
            self.image=pygame.transform.flip(self.image,True,False)

    def reverse(self): # di chuyển ngược lại
        self.speed*=-1
        
    # cập nhập lại vị trí và hoạt ảnh trong game
    def update(self, shift):  
        self.rect.x+=shift
        self.animated()
        self.move()
        self.reverse_image()
