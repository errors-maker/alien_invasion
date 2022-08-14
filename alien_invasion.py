import sys
from time import sleep
import pygame
import json

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_states import GameStates
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并船舰游戏资源"""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("薄纱酱鸡煜")
        # 创建实例
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.states = GameStates(self)
        self.sb = Scoreboard(self)

        # 绘制play按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.states.game_active:

                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # 监视键盘和鼠标事件。
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_play_button(self, mouse_pos):
        """玩家单击Play时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.states.game_active:
            self.states.game_active = True
            # 重置游戏的统计信息
            self.states.reset_states()
            self.sb.prep_score()

            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹并将其加入编组bullets中"""
        if self.states.game_active and len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        """检查是否有子弹击中了外星人"""
        # 如果是，删除相应子弹和外星人,并增加得分
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.states.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _create_fleet(self):
        """创建外星人群"""
        alien = Alien(self)

        # 计算屏幕能容纳多少外星人
        avaliable_space_x = self.settings.screen_width
        number_alien_x = avaliable_space_x // (2 * alien.alien_width)

        avaliable_space_y = self.settings.screen_height-self.ship.ship_height
        number_rows = avaliable_space_y // (2 * alien.alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人并将其加入当前行
        alien = Alien(self)
        alien.x = alien.alien_width + 2 * alien_number * alien.alien_width
        alien.rect.y = 0.5 * alien.rect.height + 2 * row_number * alien.rect.height

        self.aliens.add(alien)

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘更新外星人群中的所有外星人"""
        self._check_fleet_edges()
        self.aliens.update()
        # 若外星人为空则清空子弹并新建一群外星人
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.states.player_level += 1
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检查是否有外星人到达底部
        self._check_alien_bottom()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星下移并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_alien_bottom(self):
        """检查是否有外星人到达底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 类似飞船被撞处理
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船与外星人相撞事件"""
        if self.states.ship_left > 0:
            # ship_left减一
            self.states.ship_left -= 1

            # 清空余下的子弹和外星人
            self.aliens.empty()
            self.bullets.empty()

         # 创建一群新的外星人，并让飞船处于屏幕正中间
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.update_highest_score()
            self.states.game_active = False

    def update_highest_score(self):
        """在本地更新最高得分"""
        filename = 'highest_score.json'
        if self.states.score >= self.states.high_score:
            with open(filename, 'w') as file_object:
                json.dump(self.states.score, file_object)

    def _update_screen(self):
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()
        # 显示玩家等级
        self.sb.show_player_level()
        if not self.states.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见。
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()
