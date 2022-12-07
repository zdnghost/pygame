import pygame 
from support import import_folder

import projectiles

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # dust particles 
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 10
        self.gravity = 0.8
        self.jump_speed = -18

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.is_shooting = False

        #player attack
        self.shooting_speed = 750
        self.bullet_speed = 20 
        self.bullet_range = 800
        self.bullet_offset = pygame.math.Vector2(10,-5)
        #time
        self.clock = pygame.time.Clock()
        self.time = 0

    def import_character_assets(self):
        character_path = 'graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'idle-shoot':[],'run-shoot':[],'fall-shoot':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = pygame.transform.scale(animation[int(self.frame_index)],(64,64))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust_particle,pos)

    def get_input(self):
        keys=pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x=-1
            self.facing_right=False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x=1
            self.facing_right=True
        else:
            self.direction.x=0
        
        if keys[pygame.K_SPACE]and self.on_ground:
            self.jump()

        if keys[pygame.K_f]:
            self.is_shooting=True
            self.shoot()
        else:
            self.is_shooting=False

    def get_status(self):
        if self.direction.y<-0.2:
            self.status='jump'
        elif self.direction.y>1:
            self.status='fall'
        else:
            if self.direction.x!=0:
                if(self.is_shooting):
                    self.status='run-shoot'
                else:
                    self.status='run'
            else: 
                if(self.is_shooting):
                    self.status='idle-shoot'
                else:
                    self.status='idle'
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def shoot(self):
        if(self.time>self.shooting_speed):
            if(self.facing_right):
                bullet = projectiles.Projectile(self.rect.center+self.bullet_offset,"graphics/projectiles/bullet",self.bullet_speed,self.bullet_range)

            else:
                bullet = projectiles.Projectile(self.rect.center+pygame.math.Vector2(-self.bullet_offset.x,self.bullet_offset.y),"graphics/projectiles/bullet",-self.bullet_speed,self.bullet_range)

            projectiles.player_projectiles.add(bullet)
            self.time-=self.shooting_speed

    def update(self):
        #update time
        self.time+=self.clock.tick()  

        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        


