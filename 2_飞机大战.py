# -*- coding: utf-8 -*-
# @Time : 2020/2/21 15:11
# @Author : zhu
# @FileName: 1_窗口的创建.py
# @Software: PyCharm
import os
import random
import pygame
import time

# 1、设置变量
width = 360
height = 480
fps = 60

# 初始化pygame模块
pygame.init()
# 初始化声音模块
pygame.mixer.init()

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# 创建一个窗口(窗口大小以元组的方式传入，宽高)
screen = pygame.display.set_mode((width,height))
# 设置窗口的标题
pygame.display.set_caption("飞机大战")
# 获取时钟
clock = pygame.time.Clock()

# 图片路径拼接
path = os.getcwd()
img_path = os.path.join(path, "img")
plane_image = pygame.image.load(os.path.join(img_path, "playerShip1_orange.png")).convert()

enemy_image = []
for i in ["meteorBrown_big1.png","meteorBrown_big2.png","meteorBrown_med1.png","meteorBrown_med3.png","meteorBrown_small1.png","meteorBrown_small2.png","meteorBrown_tiny1.png"]:
    enemy_image.append(pygame.image.load(os.path.join(img_path, i)).convert())

bubble_image = pygame.image.load(os.path.join(img_path, "laserRed16.png")).convert()
background_image = pygame.image.load(os.path.join(img_path, "starfield.png")).convert()
background_rect = background_image.get_rect()

# 爆炸效果图片
explosion_dic = {}
explosion_dic["regular_ex"] = []
explosion_dic["small_ex"] = []
explosion_dic["player_ex"] = []
for i in range(0, 9):
    image = pygame.image.load(os.path.join(img_path, f"regularExplosion0{i}.png")).convert()
    image.set_colorkey(black)
    regularex_image = pygame.transform.scale(image, (75, 75))
    explosion_dic["regular_ex"].append(regularex_image)

    smallex_image = pygame.transform.scale(image, (25, 25))
    explosion_dic["small_ex"].append(smallex_image)

    player_image = pygame.image.load(os.path.join(img_path, f"sonicExplosion0{i}.png")).convert()
    player_image.set_colorkey(black)
    player_image = pygame.transform.scale(image, (75, 75))
    explosion_dic["player_ex"].append(player_image)

# 音乐路径拼接
mpath = os.path.join(path, "snd")
shoot_sound = pygame.mixer.Sound(os.path.join(mpath, "pew.wav"))
shoot_sound.set_volume(0.1)
boom_sound = []
for i in ["expl3.wav", "expl3.wav"]:
    pygame.mixer.Sound(os.path.join(mpath, i)).set_volume(0.1)
    boom_sound.append(pygame.mixer.Sound(os.path.join(mpath, i)))

# 背景音乐
pygame.mixer.music.load(os.path.join(mpath, "Phoenix.flac"))
pygame.mixer.music.set_volume(1)  # 调节音量大小
pygame.mixer.music.play(loops=-1) # 无限循环背景音乐

# 战机类
class Plane(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # 精灵必要的两个要素：图片和矩阵信息
        # 改变图片的大小 pygame.transform.scale()
        self.image = pygame.transform.scale(plane_image, (70, 50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.blood = 100
        self.shoot_time = pygame.time.get_ticks()

        self.radius = self.radius = int(self.rect.width/2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)

        self.rect.center = (width/2, height-self.rect.height/2)

    # 定义更新的方法
    def update(self, *args):
        # 使精灵位置变化的操作
        key_status = pygame.key.get_pressed()
        self.speed = 6

        if key_status[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_status[pygame.K_DOWN]:
            self.rect.y += self.speed
        if key_status[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_status[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_status[pygame.K_SPACE]:
            self.shoot()


        # 边界判断
        if self.rect.x >= width - self.rect.width:
            self.rect.x = width - self.rect.width
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= height - self.rect.height:
            self.rect.y = height - self.rect.height
        if self.rect.y <= 0:
            self.rect.y = 0

    # 射击方法
    def shoot(self):
        shoot_delay = 250
        now = pygame.time.get_ticks()
        if now - self.shoot_time >= shoot_delay:
            self.shoot_time = now
            bubble = Bubble(self.rect.centerx, self.rect.y)
            all_spirits.add(bubble)
            bubble_spirits.add(bubble)
            shoot_sound.play()

# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 精灵必要的两个要素：图片和矩阵信息
        self.image = random.choice(enemy_image)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width * .85/2)
        # pygame.dra w.circle(self.image, red, self.rect.center, self.radius)

        self.rect.x = random.randint(0,width-self.rect.width)
        self.rect.y = random.randint(-500, 0)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(6, 7)

    def update(self, *args):

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.x <= 0 - self.rect.width) or (self.rect.x >= width) or (self.rect.y >= height):
            self.rect.x = random.randint(0, width - self.rect.width)
            self.rect.y = random.randint(-1000, 0)

# 子弹类
class Bubble(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bubble_image, (10, 45))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width/2
        self.rect.y = y - self.rect.height
        self.speed = 5

    def update(self, *args):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            # 对象.kill()方法就是杀掉对象，注意相当于释放了内存空间
            self.kill()

# 爆炸类
class Boom(pygame.sprite.Sprite):
    def __init__(self, size, center):
        super().__init__()

        self.size = size
        self.image = explosion_dic[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.bomm_rate = 50
        self.bomm_time = pygame.time.get_ticks()
        self.num = 0

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.bomm_time >= self.bomm_rate:
            self.bomm_time == now
            self.num += 1
            if self.num == len(explosion_dic[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_dic[self.size][self.num]
                self.rect = self.image.get_rect()
                self.rect.center = center


# 实例化一个精灵
plane = Plane()

# pygame提供一个精灵集合，统一管理精灵
all_spirits = pygame.sprite.Group()
enemy_spirits = pygame.sprite.Group()
bubble_spirits = pygame.sprite.Group()
all_spirits.add(plane)

def draw_text(screen, text, color, x, y, size):
    # 定义绘制文字
    font = pygame.font.Font(None, size)
    # 在pygame中其实是绘制图片，文字的图片
    font_image = font.render(str(text), True, color)
    # 获取矩阵
    font_rect = font_image.get_rect()
    # 设置坐标
    font_rect.center = (x, y)
    # 绘制图片
    screen.blit(font_image, font_rect)

def draw_blood(screen, x, y, blood):
    if blood <= 0:
        blood = 0
    width = 100
    height = 20
    # 绘画矩形
    # 获取矩形
    out_rect = pygame.Rect(x, y, width, height)
    in_rect = pygame.Rect(x, y, blood, height)
    # 绘制矩形
    pygame.draw.rect(screen,white,out_rect,2)
    pygame.draw.rect(screen,green,in_rect)

# 实例化敌人
def new_enemy():
    enemy = Enemy()
    all_spirits.add(enemy)
    enemy_spirits.add(enemy)

# 实例化十个敌人
for i in range(15):
    new_enemy()

running = True
score = 0
# 游戏的主体
while running:

    # 控制每秒的帧数
    clock.tick(fps)
    # 监测
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # 更新
    all_spirits.update()

    # 飞机和敌人之间的碰撞检测，布尔值决定发生碰撞后敌人是否消失
    hits = pygame.sprite.spritecollide(plane, enemy_spirits, True, pygame.sprite.collide_circle)
    for hit in hits:
        boom = Boom("small_ex", hit.rect.center)
        all_spirits.add((boom))
        random.choice(boom_sound).play()
        plane.blood -= 10
        new_enemy()
        if plane.blood == 0:
            player_boom = Boom("player_ex", plane.rect.center)
            all_spirits.add((player_boom))
            plane.kill()

    if not plane.alive() and not player_boom.alive():
        running = False


    hits = pygame.sprite.groupcollide(enemy_spirits, bubble_spirits, True, True)
    for hit in hits:
        score += 150 - hit.rect.width
        boom = Boom("regular_ex", hit.rect.center)
        all_spirits.add((boom))
        new_enemy()
        random.choice(boom_sound).play()

    # 渲染
    screen.fill(green)
    screen.blit(background_image, background_rect)
    draw_text(screen, score, red, 50, 30, 30)
    draw_blood(screen, 250, 17, plane.blood)
    all_spirits.draw(screen)
    pygame.display.flip()