import sys

import pygame

from bullet import Bullet

from alien import Alien

from time import sleep




def fire_bullet(ai_settings, screen, ship, bullets):
    """如果子弹没有达到限制，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    # 限制子弹个数
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)  # 创建new_bullet实例
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets,
                      ai_settings, screen, ship, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets,
                      ai_settings, screen, ship, sb):
    """"在玩家单机play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        if play_button.rect.collidepoint(mouse_x, mouse_y):
            # 重置游戏统计信息
            stats.reset_stats()
            stats.game_active = True

            # 重置记分牌图像
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_beat_number()
            sb.prep_ships()

            # 清空外星人列表和子弹列表
            aliens.empty()
            bullets.empty()

            # 创建一群新的外星人，并让飞船居中
            create_fleet(ai_settings, screen, aliens)

            ship.center_ship


def create_fleet(ai_settings, screen, aliens):
    number_aliens_x = 1
    for alien_number in range(number_aliens_x):
        alien = Alien(ai_settings, screen)
        alien.rect.x = alien.location
        aliens.add(alien)


def update_bullets(bullets, aliens, ai_settings, screen, stats, sb):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()            # bullets = Group()→bullets.add(new_bullet)→new_bullet = Bullet(ai_settings, screen, ship)→→bullets拥有了Bullet的属性

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人

    check_bullet_alien_collisions(ai_settings, screen, stats,
                                  sb, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats,
                                  sb, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_point * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # 删除现有的子弹，并创建一个新的外星人
        # 如果外星人被消灭，就将击落数量+1
        bullets.empty()
        sleep(0.1)
        ai_settings.increase_speed()
        # 提高等级
        stats.beat_number += 1
        sb.prep_beat_number()
        create_fleet(ai_settings, screen, aliens)


def check_alien_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_alien_direction(ai_settings)
            break


# def check_alien_y(ai_settings, screen, aliens):
#     """检测出场外星人向下移动的情况"""
#     for alien in aliens.sprites():
#         if len(aliens) < 2:
#             create_fleet(ai_settings, screen, aliens)
#             break


def change_alien_direction(ai_settings):
    """将外星人向下移动，并在触壁后改变运动方向"""
    ai_settings.alien_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """检查是否有外星人位于屏幕边缘，并更新外星人位置"""
    check_alien_edges(ai_settings, aliens)
    # check_alien_y(ai_settings, screen, aliens)
    aliens.update(ai_settings)

    # 检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ship_left减1
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """"检查是否诞生了最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)   # screen.fill()是pygame的一个函数（方法），只接受一个实参→颜色
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就会绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

