import json


class GameStates():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        # 获取本地最高得分
        self.high_score = 0
        filename = 'highest_score.json'
        try:
            with open(filename) as file_object:
                self.high_score = json.load(file_object)
        except FileNotFoundError:
            pass
        # 游戏开始时处于活动状态
        self.game_active = False
        self.reset_states()

    def reset_states(self):
        # 初始化在游戏运行期间可能变化的统计信息
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.player_level = 1
