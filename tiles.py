from support import import_folder
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image=pygame.Surface((size,size))
        self.rect=self.image.get_rect(topleft=(x,y))
    def update(self,shift):
        self.rect.x+=shift
    
class StaticTile(Tile):
    def __init__(self, size, x, y,surface):
        super().__init__(size, x, y)
        self.image=surface
class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y,pygame.image.load('graphics/terrain/crate.png').convert_alpha())
        offset_y=y+size
        self.rect=self.image.get_rect(bottomleft=(x,offset_y))

class AnimatedTile(Tile):
    def __init__(self, size, x, y,path):
        super().__init__(size, x, y)
        self.frames=import_folder(path)
        self.frames_index=0
        self.image=self.frames[self.frames_index]
    
    def animated(self):
        self.frames_index+=0.15
        if self.frames_index>=len(self.frames):
            self.frames_index=0
        self.image=self.frames[int(self.frames_index)]

    def update(self, shift):
        self.animated()
        self.rect.x+=shift
class Coin(AnimatedTile):
    #class const
    goldType="gold_coin"
    silverType = "silver_coin"

    #tao group cho coin
    coinGroup = pygame.sprite.Group()

    def __init__(self, size, x, y, path,coin_type):
        super().__init__(size, x, y, path)
        center_x=x+int(size/2)
        center_y=y+int(size/2)
        self.rect=self.image.get_rect(center=(center_x,center_y))

        #them coin vao group
        Coin.coinGroup.add(self)
        self.coinType = coin_type

class Palm(AnimatedTile):
    def __init__(self, size, x, y, path,offset):
        super().__init__(size, x, y, path)
        offset_y=y-offset
        self.rect.topleft=(x,offset_y)
        
