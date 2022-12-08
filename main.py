import pygame, sys
pygame.init() # khởi tạo pygame


from setting import *
from level import Level
from game_data import levels

from world import World


screen=pygame.display.set_mode((screen_width,screen_height)) 
# khởi tạo cửa sổ với chiều cao, chiều dài 

clock=pygame.time.Clock() # tạo biến FPS

class Game:
    def __init__(self):# hàm thiết lập ban đầu
        self.max_level = 3 # số dòng được mở khóa ban đầu (sau khi hoàn thành 1 dòng sẽ tăng thêm)
        self.world = World(0,self.max_level,screen,self.create_level)# khởi tạo menu chọn level từ class world(tạo level)
        self.status='level_select'# khai báo cho hàm run, tình trạng ban đầu khi mới chạy là ở chọn level
        
        
        #level là màn chơi, world là menu chọn level
    def create_level(self,current_level):# chuyển sang màn chơi
        self.status='ingame' #chuyển status lại vào ingame
        self.level=Level(levels[current_level],screen,self.create_world,current_level)# gọi tạo level từ file level class Level

    def create_world(self,current_level,win_result):# chuyển sang chọn level
        if(win_result=='win'): # nếu game thắng, mở khóa dòng
            if self.max_level<current_level+1:
                self.max_level=current_level+1
        self.status='level_select' #chuyển status lại vào chọn màn chơi
        self.world = World(current_level,self.max_level,screen,self.create_level)# gọi tạo world(menu) từ file world class world

    def run(self):# hàm chạy game
        if(self.status=='level_select'):# nếu mà tình trạng hiện tại đang trong menu
            self.world.run()
        elif self.status=='ingame':# nếu mà tình trạng hiện tại đang trong game
            self.level.run()

game = Game()# tạo 1 đối tượng game

while True:# tạo vòng lặp game (vô game)
    for event in pygame.event.get(): # khởi tạo sự kiện khi bấm nút X để thoát game
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit() 
    screen.fill('black')
    game.run()# chạy hàm chạy game
    
    pygame.display.update()# cập nhập vòng lặp game liên tục
    
    clock.tick(45) # khởi tạo fps cuối