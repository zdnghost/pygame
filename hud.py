import pygame
from tiles import Coin

class Hud:
    def __init__(self,font,player) -> None:
        self.player = player
        self.font = font
        
        self.points_display = Points_Display(self.font,(100,50))
        self.coin_points = 0

    
    def checkForCoinCollision(self):
        for coin in Coin.coinGroup:
            if(pygame.Rect.collidepoint(self.player.rect,coin.rect.center[0],coin.rect.center[1])):
                #xoa coin
                coin.kill()
                if(coin.coinType==Coin.goldType):
                    self.coin_points+=3
                elif(coin.coinType==Coin.silverType):
                    self.coin_points+=1

    def update(self):
        self.checkForCoinCollision()
        self.points_display.update(self.coin_points)

    def draw(self,display_surface):
        self.points_display.draw(display_surface)

class Points_Display:
    def __init__(self,font,pos):
        self.pos = pos
        self.font = font

    def update(self,points):
        self.text=self.font.render("Coins: "+str(points),True,"white")

    def draw(self,display_surface):
        display_surface.blit(self.text,self.text.get_rect(center=self.pos))
