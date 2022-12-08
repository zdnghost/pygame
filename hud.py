import pygame
from tiles import Coin

class Hud:
    def __init__(self,font,player) -> None:
        self.player = player
        self.font = font
        
        self.points_display = Points_Display(self.font,(100,50))
        self.coin_points = 0
        
        self.health_points = 3
        self.health_display = Health_Display((50,100),self.health_points)

    
    def checkForCoinCollision(self):
        for coin in Coin.coinGroup:
            if(pygame.Rect.collidepoint(self.player.rect,coin.rect.center[0],coin.rect.center[1])):
                #xoa coin
                coin.kill()
                if(coin.coinType==Coin.goldType):
                    self.coin_points+=3
                elif(coin.coinType==Coin.silverType):
                    self.coin_points+=1

    def update(self,health_count):
        self.checkForCoinCollision()
        self.points_display.update(self.coin_points)
        self.health_display.update(health_count)

    def draw(self,display_surface):
        self.points_display.draw(display_surface)
        self.health_display.draw(display_surface)

class Points_Display:
    def __init__(self,font,pos):
        self.pos = pos
        self.font = font

    def update(self,points):
        self.text=self.font.render("Coins: "+str(points),True,"white")

    def draw(self,display_surface):
        display_surface.blit(self.text,self.text.get_rect(center=self.pos))

class Health_Display:
    def __init__(self,pos,health_count):
        self.heart_offset = 30
        self.pos = pos
        self.health_count = health_count
        self.heart_group = pygame.sprite.Group()

        for i in range(self.health_count):
            heart = Heart((self.pos[0]+self.heart_offset*i,self.pos[1]),(30,30))
            self.heart_group.add(heart)
    


    def update(self,health_count):
        if health_count<self.health_count:
            for index,heart in enumerate(self.heart_group):
                if index == self.health_count-1:
                    heart.kill()
        elif health_count>self.health_count:
            heart = Heart((self.pos[0]+self.heart_offset*(health_count-1),self.pos[1]),(30,30))
            self.heart_group.add(heart)

            
    def draw(self,display_surface):
        self.heart_group.draw(display_surface)


class Heart(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('graphics/hud/heart.png')
        self.image = pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect(center = pos)