from decimal import Rounded
import pygame.font


class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示计分板的属性"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.states = ai_game.states

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像和最高分图像
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        score = round(self.states.score, -1)
        score_str = "{:,}".format(score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为图像"""
        high_score = round(self.states.high_score, -1)
        high_score_str = "{:,}". format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)

        # 将最高得分在屏幕顶部显示
        self.high_score_rect = self.score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def show_player_level(self):
        """在屏幕上显示玩家等级"""
        level = self.states.player_level
        level_str = "{:,}". format(level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.top + 50
        self.level_rect.right = self.score_rect.right
        self.screen.blit(self.level_image, self.level_rect)

    def check_high_score(self):
        """检查当前得分是否超过最高分"""
        if self.states.score >= self.states.high_score:
            self.states.high_score = self.states.score
            self.prep_high_score()
