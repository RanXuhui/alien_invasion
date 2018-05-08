import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (255, 0, 30)
        self.font = pygame.font.SysFont(None, 25)

        # 准备记分板文字
        self.prep_letter()
        # 准备初始的得分图像
        self.prep_score()
        # 准备包含最高得分和当前得分的图像
        self.prep_high_score()
        # 准备显示击落的外星人数量
        self.prep_beat_number()
        self.prep_ships()

    def prep_letter(self):
        letter_score = 'score:'
        letter_high_score = 'highest score:'
        letter_beat_number = 'beat number:'
        self.letter_score_image = self.font.render(letter_score, True, self.text_color,
                                            self.ai_settings.bg_color)
        self.letter_high_score_image = self.font.render(letter_high_score, True, self.text_color,
                                                   self.ai_settings.bg_color)
        self.letter_beat_number_image = self.font.render(letter_beat_number, True, self.text_color,
                                                   self.ai_settings.bg_color)
        self.letter_score_rect = self.letter_score_image.get_rect()
        self.letter_score_rect.right = self.screen_rect.right - 150
        self.letter_score_rect.top = 20

        self.letter_high_score_rect = self.letter_high_score_image.get_rect()
        self.letter_high_score_rect.centerx = self.screen_rect.centerx - 180
        self.letter_high_score_rect.top = self.letter_score_rect.top

        self.letter_beat_number_rect = self.letter_beat_number_image.get_rect()
        self.letter_beat_number_rect.right = self.letter_score_rect.right - 2
        self.letter_beat_number_rect.top = self.letter_score_rect.bottom + 10



    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)
        # 将得分放在放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color,
                                                 self.ai_settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_beat_number(self):
        """将击落的飞机数量转换为渲染的图像"""
        self.beat_number_image = self.font.render(str(self.stats.beat_number), True,
                                                 self.text_color,
                                                 self.ai_settings.bg_color)

        # 将数量放在得分的下方
        self.beat_number_rect = self.beat_number_image.get_rect()
        self.beat_number_rect.right = self.score_rect.right
        self.beat_number_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还余下多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.beat_number_image, self.beat_number_rect)
        self.screen.blit(self.letter_score_image, self.letter_score_rect)
        self.screen.blit(self.letter_high_score_image, self.letter_high_score_rect)
        self.screen.blit(self.letter_beat_number_image, self.letter_beat_number_rect)
        self.ships.draw(self.screen)