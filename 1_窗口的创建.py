# -*- coding: utf-8 -*-
# @Time : 2020/2/21 15:11
# @Author : zhu
# @FileName: 1_窗口的创建.py
# @Software: PyCharm

import pygame

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
pygame.time.Clock()


running = True
# 游戏的主体
while running:

    # 监测
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill(white)
    pygame.display.flip()