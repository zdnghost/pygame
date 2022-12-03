import pygame, sys
from setting import *
from level import Level
from game_data import levels

from world import World

pygame.init()
screen=pygame.display.set_mode((screen_width,screen_height))
clock=pygame.time.Clock()

class Game:
    def __init__(self):
        self.max_level = 5
        self.world = World(1,self.max_level,screen,self.create_level)
        self.status='level_select'
    
    def create_level(self,current_level):
        self.status='in_game'
        self.level=Level(levels[current_level],screen)
        pass

    def run(self):
        if(self.status=='level_select'):
            self.world.run()
        else:
            self.level.run()

game = Game()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit() 
    screen.fill('black')
    game.run()
    pygame.display.update()
    clock.tick(60)