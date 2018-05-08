import pygame
import random
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人的起始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # self.screen_rect = screen.get_rect()
        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/pig.bmp')
        self.rect = self.image.get_rect()
        # 随机位置生成外星人
        self.location = random.uniform(self.rect.width, ai_settings.screen_width - self.rect.width)

        # 每个外星人的初始位置
        self.rect.x = self.location
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def check_y(self):
        if self.y > 150:
            return True
        # elif self.y > 120:
        #     return False
        else:
            return False

    def update(self, ai_settings):
        """向左右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.alien_direction)
        self.rect.x = self.x
        self.y += ai_settings.alien_drop_speed
        self.rect.y = self.y

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)