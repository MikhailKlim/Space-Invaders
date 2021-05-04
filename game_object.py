import pygame
from random import *
from level import *
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.change_x = 0.0
        self.change_y = 0.0
        self.speed = 12.0
        self.control_type = 'mouse'
        self.last_cur_x = 0
        self.last_cur_y = 0
        self.direction_ver = ""
        self.direction_gor = ""
        self.flying_frames = []
        image = pygame.image.load('images/razor/razorinv_1.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/razor/razorinv_2.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/razor/razorinv_3.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/razor/razorinv_4.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/razor/razorinv_5.png').convert_alpha()
        self.flying_frames.append(image)

        self.image = self.flying_frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.res_pos = []
        self.anim_speed = 2
        self.animation = 0
        self.time1 = 0
        self.cooldown = 0
        self.moving = None
        self.fire_rate = 2.5
        self.pl_bullets = pygame.sprite.Group()
        self.pl_anim_cld = (FPS/self.anim_speed)//len(self.flying_frames)

    def shot(self):
        bullet = Bullet(self.rect.centerx, self.rect.y)
        self.pl_bullets.add(bullet)
        
    def update(self):
        calc_speed = 0.0
        if self.control_type == 'mouse':
            pos_x, pos_y = pygame.mouse.get_pos()
            if self.last_cur_x != pos_x or self.last_cur_y != pos_y:
                self.moving = True
            elif pos_x < self.last_cur_x and pos_y < self.last_cur_y:
                self.moving = False
            self.last_cur_x = pos_x
            self.last_cur_y = pos_y
            dis_x = pos_x - self.rect.centerx
            dis_y = pos_y - self.rect.centery
            if self.moving:
                if abs(dis_x) > abs(dis_y):
                    if dis_y != 0:
                        calc_speed = abs(dis_x/dis_y)
                        change_var1 = (self.speed/(calc_speed+1))*calc_speed
                        change_var2 = self.speed - change_var1
                        self.change_y = change_var2
                        self.change_x = change_var1
                    elif dis_y == 0:
                        self.change_x = self.speed
                        self.change_y = 0
                elif abs(dis_y) > abs(dis_x):
                    if dis_x != 0:
                        calc_speed = abs(dis_y/dis_x)
                        change_var1 = (self.speed/(calc_speed+1))*calc_speed
                        change_var2 = self.speed - change_var1
                        self.change_x = change_var2
                        self.change_y = change_var1
                    elif dis_x == 0:
                        self.change_y = self.speed
                        self.change_x = 0
                elif abs(dis_y) == abs(dis_x):
                    self.change_y = self.speed/1.5
                    self.change_x = self.speed/1.5
            if dis_x > 0:
                if self.rect.centerx <= 775:
                    if abs(dis_x) >= self.change_x:
                        self.rect.centerx += self.change_x
                    else:
                        self.rect.centerx += dis_x
            if dis_x < 0:
                if self.rect.centerx >= 25:
                    if abs(dis_x) >= self.change_x:
                        self.rect.centerx -= self.change_x
                    else:
                        self.rect.centerx += dis_x
            if dis_y > 0:
                if self.rect.centery <= 775:
                    if abs(dis_y) >= self.change_y:
                        self.rect.centery += self.change_y
                    else:
                        self.rect.centery += dis_y
            if dis_y < 0:
                if self.rect.centery >= 245:
                    if abs(dis_y) >= self.change_y:
                        self.rect.centery -= self.change_y
                    else:
                        self.rect.centery += dis_y
            self.last_cur_x = pos_x
            self.last_cur_y = pos_y

        elif self.control_type == 'WASD':
            if self.speed == abs(self.change_x) and abs(self.change_y):
                self.change_x /= 2
                self.change_y /= 2
            self.rect.centery += self.change_y
            self.rect.centerx += self.change_x
            if self.direction_gor == 'R' and self.rect.x >= 750:
                self.rect.centerx -= self.change_x
            if self.direction_gor == 'L' and self.rect.x <= 0:
                self.rect.centerx -= self.change_x
            if self.direction_ver == 'D' and self.rect.y >= 750:
                self.rect.centery -= self.change_y
            if self.direction_ver == 'U' and self.rect.y <= 270:
                self.rect.centery -= self.change_y
        self.time1 += 1
        if self.time1 == self.pl_anim_cld:
            self.time1 = 0
            self.animation += 1
            if self.animation < len(self.flying_frames):
                self.image = self.flying_frames[self.animation]
            else:
                self.animation = 0
                self.image = self.flying_frames[self.animation]
        if self.cooldown >= 0:
            self.cooldown -= self.fire_rate

    def draw(self, screen):
        pass

    def go_left(self):
        self.change_x = -self.speed + 4
        self.direction_gor = "L"

    def go_right(self):
        self.change_x = self.speed - 4
        self.direction_gor = "R"

    def go_up(self):
        self.change_y = -self.speed + 4
        self.direction_ver = "U"

    def go_down(self):
        self.change_y = self.speed - 4
        self.direction_ver = "D"

    def stop(self, direct):
        if direct == 'gor':
            self.change_x = 0
        if direct == 'ver':
            self.change_y = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=0, speed=-18, speed_x=0, img='images/bullet.png', bul_type='friend'):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = radius
        self.speed = speed
        self.speed_x = speed_x
        self.bul_type = bul_type

    def update(self):
        if self.rect.y <= 0 or self.rect.y >= 800:
            self.kill()
        if self.rect.x <= 0 or self.rect.x >= 800:
            self.kill()
        self.rect.y += self.speed
        self.rect.x += self.speed_x

class Bomb(Bullet):
    def __init__(self, x, y, radius=randint(400, 700), speed=7, speed_x=0, img='images/EnergyBomb.png', bul_type='enemy'):
        super().__init__(x, y)
        self.en_bullets = pygame.sprite.Group()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = radius
        self.speed = speed
        self.speed_x = speed_x
        self.bul_type = bul_type

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.speed_x

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, fire_rate=0.9, hp=2, anim_speed=1):
        super().__init__()
        self.flying_frames = []
        self.en_bullets = pygame.sprite.Group()
        image = pygame.image.load('images/gr.invader/Greeninvader.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/gr.invader/Greeninvader2.png').convert_alpha()
        self.flying_frames.append(image)
        self.image = self.flying_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start = x
        self.stop = x
        self.stop2 = y
        self.direction = 1
        self.time1 = 0
        self.animation = 0
        self.anim_speed = anim_speed
        self.fire_rate = fire_rate
        self.speed = speed
        self.hp = hp
        self.anim_cld = (FPS/self.anim_speed)//len(self.flying_frames)
        self.cooldown = FPS

    def update(self):
        self.cooldown -= self.fire_rate
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1
        self.rect.x += self.direction * self.speed
        self.time1 += 1
        if self.time1 == self.anim_cld:
            self.time1 = 0
            self.animation += 1
            if self.animation < len(self.flying_frames):
                self.image = self.flying_frames[self.animation]
            else:
                self.animation = 0
                self.image = self.flying_frames[self.animation]
        if self.hp <= 0:
            self.kill()
        if self.cooldown <= 0:
            self.shot()
        

class Green_invader(Enemy):
    def __init__(self, x, y, speed=4, hp=2, fire_rate=0.9, anim_speed=1):
        super().__init__(x, y)
        self.flying_frames = []
        self.en_bullets = pygame.sprite.Group()
        image = pygame.image.load('images/gr.invader/Greeninvader.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/gr.invader/Greeninvader2.png').convert_alpha()
        self.flying_frames.append(image)
        self.image = self.flying_frames[0]
        self.fire_rate = fire_rate
        self.speed = speed
        self.anim_speed = anim_speed
        self.anim_cld = (FPS/self.anim_speed)//len(self.flying_frames)
        self.hp = hp
        
    def shot(self):
        self.cooldown = FPS
        bullet = Bullet(self.rect.centerx, self.rect.y, 800, 6, 0, 'images./grBullet.png', 'enemy')
        self.en_bullets.add(bullet)
            

class Blue_invader(Enemy):
    def __init__(self, x, y, speed=4, hp=4, fire_rate=0.7, anim_speed=1):
        super().__init__(x, y)
        self.flying_frames = []
        self.en_bullets = pygame.sprite.Group()
        image = pygame.image.load('images/bl.invader/Blueinvader.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/bl.invader/Blueinvader2.png').convert_alpha()
        self.flying_frames.append(image)
        self.image = self.flying_frames[0]
        self.fire_rate = fire_rate
        self.speed = speed
        self.anim_speed = anim_speed
        self.anim_cld = (FPS/self.anim_speed)//len(self.flying_frames)
        self.hp = hp
        self.side_gun_pos_x = 45
        self.side_gun_pos_y = 30

    def shot(self):
        self.cooldown = FPS
        self.side_gun_pos = 45
        for i in range(2): 
            bullet = Bullet(self.rect.centerx+self.side_gun_pos, self.rect.y+self.side_gun_pos_y, 800, 10, 0, 'images./blBullet.png', 'enemy')
            self.en_bullets.add(bullet)
            self.side_gun_pos *= -1


class Red_invader(Enemy):
    def __init__(self, x, y, speed=6, hp=3, fire_rate=0.6, anim_speed=1.5):
        super().__init__(x, y)
        self.flying_frames = []
        self.en_bullets = pygame.sprite.Group()
        image = pygame.image.load('images/red.invader/Redinvader.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/red.invader/Redinvader2.png').convert_alpha()
        self.flying_frames.append(image)
        self.image = self.flying_frames[0]
        self.fire_rate = fire_rate
        self.speed = speed
        self.anim_speed = anim_speed
        self.anim_cld = (FPS/self.anim_speed)//len(self.flying_frames)
        self.hp = hp
        
    def shot(self):
        self.cooldown = FPS
        bullet_angle = -4.5
        for i in range(6): 
            bullet = Bullet(self.rect.centerx, self.rect.y, 800, 7, bullet_angle, 'images./redBullet.png', 'enemy')
            self.en_bullets.add(bullet)
            bullet_angle += 1.5

class Volt(Enemy):
    def __init__(self, x, y, speed=7, hp=10, fire_rate=6, anim_speed=2.3):
        super().__init__(x, y)
        self.flying_frames = []
        self.bombs = pygame.sprite.Group()
        self.en_bullets = pygame.sprite.Group()
        image = pygame.image.load('images/volt/norm_volt/volt.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/volt/norm_volt/volt2.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/volt/norm_volt/volt3.png').convert_alpha()
        self.flying_frames.append(image)
        image = pygame.image.load('images/volt/norm_volt/volt4.png').convert_alpha()
        self.flying_frames.append(image)
        self.image = self.flying_frames[0]
        self.fire_rate = fire_rate
        self.speed = speed
        self.anim_speed = anim_speed
        self.anim_cld = (FPS/self.anim_speed)//len(self.flying_frames)
        self.hp = hp
        self.hp_max = self.hp
        self.active_gun = 'right'
        self.side_gun_pos_x = 45
        self.side_gun_pos_y = 30
        self.bomb_cld = FPS
        self.rage = False
        self.bullet_spd = 8
        self.bomb_spd = 7

    def update(self):
        if not self.rage:
            self.hp_check()
        self.cooldown -= self.fire_rate
        self.bomb_cld -= self.fire_rate/15
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1
        self.rect.x += self.direction * self.speed
        self.time1 += 1
        if self.time1 == self.anim_cld:
            self.time1 = 0
            self.animation += 1
            if self.animation < len(self.flying_frames):
                self.image = self.flying_frames[self.animation]
            else:
                self.animation = 0
                self.image = self.flying_frames[self.animation]
        if self.hp <= 0:
            self.kill()
        if self.cooldown <= 0:
            self.shot()
        if self.bomb_cld <= 0:
            self.bomb_shot()
        for i in self.bombs:
            if i.rect.y >= i.radius:
                angle_x = 7
                angle_y = 7
                for j in range(2):
                    x, y = i.rect.centerx, i.rect.y
                    z = 1
                    for n in range(2): 
                        bullet = Bullet(x, y+(10*z), 800, 0, angle_x, 'images./redBullet.png', 'enemy')
                        self.en_bullets.add(bullet)
                        z *= -1
                    angle_x *= -1
                for j in range(2):
                    x, y = i.rect.centerx, i.rect.y
                    z = 1
                    for n in range(2): 
                        bullet = Bullet(x+(10*z), y, 800, angle_y, 0, 'images./redBullet.png', 'enemy')
                        self.en_bullets.add(bullet)
                        z *= -1
                    angle_y *= -1
                bullet = Bullet(i.rect.centerx, i.rect.y, 800, -angle_x/2, angle_x/2, 'images./redBullet.png', 'enemy')
                self.en_bullets.add(bullet)
                bullet = Bullet(i.rect.centerx, i.rect.y, 800, angle_x/2, -angle_x/2, 'images./redBullet.png', 'enemy')
                self.en_bullets.add(bullet)
                bullet = Bullet(i.rect.centerx, i.rect.y, 800, angle_x/2, angle_x/2, 'images./redBullet.png', 'enemy')
                self.en_bullets.add(bullet)
                bullet = Bullet(i.rect.centerx, i.rect.y, 800, -angle_x/2, -angle_x/2, 'images./redBullet.png', 'enemy')
                self.en_bullets.add(bullet)
                i.kill()


    def shot(self):
        self.cooldown = FPS
        angle_y = randint(4, self.bullet_spd)
        angle_x = self.bullet_spd - angle_y
        if self.active_gun == 'left':
            self.side_gun_pos_x = 45
            self.active_gun = 'right'
        elif self.active_gun == 'right':
            self.side_gun_pos_x = -45
            self.active_gun = 'left'
        if not self.rage:
            bullet = Bullet(self.rect.centerx+self.side_gun_pos_x, self.rect.y+self.side_gun_pos_y, 800, self.bullet_spd, 0, 'images/voltBullet.png', 'enemy')
        elif self.rage:
            bullet = Bullet(self.rect.centerx+self.side_gun_pos_x, self.rect.y+self.side_gun_pos_y, 800, angle_y, angle_x, 'images/voltBullet.png', 'enemy')
        self.en_bullets.add(bullet)

    def bomb_shot(self):
        self.bomb_cld = FPS
        if self.rage:
            n = 1
            for i in range(2):
                bomb = Bomb(self.rect.centerx, self.rect.y, randint(400, 700), self.bomb_spd, self.bomb_spd/4.5*n, 'images/EnergyBomb.png', 'enemy')
                self.en_bullets.add(bomb)
                self.bombs.add(bomb)
                n *= -1
        elif not self.rage:
            bomb = Bomb(self.rect.centerx, self.rect.y, randint(400, 700), self.bomb_spd, 0, 'images/EnergyBomb.png', 'enemy')
            self.en_bullets.add(bomb)
            self.bombs.add(bomb)
    
    def hp_check(self):
        if self.hp < self.hp_max/10*5:
            self.rage = True
            self.bullet_spd = 10
            self.fire_rate = 6.5
            self.speed = 8
            self.flying_frames.clear()
            image = pygame.image.load('images/volt/rage_volt/voltRage.png').convert_alpha()
            self.flying_frames.append(image)
            image = pygame.image.load('images/volt/rage_volt/voltRage2.png').convert_alpha()
            self.flying_frames.append(image)
            image = pygame.image.load('images/volt/rage_volt/voltRage3.png').convert_alpha()
            self.flying_frames.append(image)
            image = pygame.image.load('images/volt/rage_volt/voltRage4.png').convert_alpha()
            self.flying_frames.append(image)
            self.image = self.flying_frames[0]