import pygame

from setting import Setting

from ship import Ship

import game_functions as gf

from pygame.sprite import Group

from ganme_stats import GameStats

from button import Button


from scoreboard import Scoreboard


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Setting()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    # 创建play按钮
    play_button = Button(ai_settings, screen, 'Play')
    # 创建存储游戏统计信息的实例， 并创建记分牌
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船,创建一个用于存储子弹的编组,创建一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    # 创建一个外星人
    # alien = Alien(ai_settings, screen)

    # 创建外星人群
    # gf.sleep_fleet(ai_settings, screen, aliens)
    gf.create_fleet(ai_settings, screen, aliens)
    # gf.create_fleet_2(ai_settings, screen, aliens)
    #开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)
        if stats.game_active:
            # 让飞船移动
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)

        # 让最近绘制的屏幕可见
        gf.update_screen(ai_settings, screen, stats, sb, ship,
                         aliens, bullets, play_button)

run_game()
