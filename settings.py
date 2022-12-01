import json

class Settings:
    def __init__(self, level_num):
        # Load Settings
        file = open("config.json")
        data = json.load(file)
        self.level_settings = data["level_settings"]
        self.player_settings = data["player_settings"]
        self.enemy_settings = data["enemy_settings"]
        self.image_settings = data["image_settings"]
        self.vfx_settings = data["vfx_settings"]
        self.sfx_settings = data["sfx_settings"]
        self.current_level = self.get_level(level_num)

    def get_level(self, level_num):
        for level_setting in self.level_settings:
            if level_setting["level"] == level_num:
                return level_setting
        return self.level_settings[0]

    def get_level_setting(self, key):
        return self.current_level[key]

    def get_player_setting(self, key):
        return self.player_settings[0][key]

    def get_enemy_setting(self, key):
        return self.enemy_settings[0][key]

    def get_image_setting(self, key):
        return self.image_settings[0][key]

    def get_vfx_setting(self, key):
        return self.vfx_settings[0][key]

    def get_sfx_setting(self, key):
        return self.sfx_settings[0][key]


