from sys import float_repr_style


class Settings():
    """存储Alien Invasion中所有设置"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1100
        self.screen_height = 700
        self.bg_color = (246, 246, 246)
        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4

        # 外星人设置
        self.fleet_drop_speed = 50

        # 加快游戏节奏
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.0
        self.bullet_speed = 1.0
        self.alien_speed = 0.13
        # 记分
        self.alien_points = 50
        # 外星人分数的提高速度
        self.score_scale = 1.5
        # fleet_direction为1表示向右，为-1表示为向左
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置和外星人分数"""
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
