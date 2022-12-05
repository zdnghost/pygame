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
        self.max_level = 3
        self.world = World(0,self.max_level,screen,self.create_level)
        self.status='level_select'
    
    def create_level(self,current_level):
        self.status='ingame'
        self.level=Level(levels[current_level],screen,self.create_world,current_level)

    def create_world(self,current_level,win_result):
        if(win_result=='win'):
            if self.max_level<current_level+1:
                self.max_level=current_level+1
        self.status='level_select'
        self.world = World(current_level,self.max_level,screen,self.create_level)

    def run(self):
        if(self.status=='level_select'):
            self.world.run()
        elif self.status=='ingame':
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