import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):    #书上不是setting是 ai_settings
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings           #self.ai_settings = ai_settings
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 游戏开始将每艘飞船放在屏幕中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom/2

        # 在飞船的属性center中存储小数值
        self.center1 = float(self.rect.centerx)
        self.center2 = float(self.rect.centery)
        # #float(self.rect.centerx)
        # #float(self.rect.centery)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def center_ship(self):
        """复活后的飞船放在屏幕底部中央"""
        self.center1 = self.screen_rect.centerx
        self.center2 = self.screen_rect.bottom - 20
        self.rect.centerx = self.center1
        self.rect.centery = self.center2
        # self.center = self.screen_rect.centerx


    def update(self):
        """根据移动标志调整飞船的位置"""
        #更新center1的值而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:       #and语句：如果前后均为‘1’(为真)时则：
            # self.rect.centerx += self.ai_settings.ship_speed_factor
            self.center1 += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            # self.rect.centerx -= self.ai_settings.ship_speed_factor
            self.center1 -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            # self.rect.centery -= self.ai_settings.ship_speed_factor
            self.center2 -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            # self.rect.centery += self.ai_settings.ship_speed_factor
            self.center2 += self.ai_settings.ship_speed_factor


        # 根据self.center更新rect对象
        self.rect.centerx = self.center1
        self.rect.centery = self.center2





    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
