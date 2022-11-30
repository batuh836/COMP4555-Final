import json

class Settings:
    def __init__(self, level):
        # Load Settings
        file = open("config.json")
        data = json.load(file)
        self.level_settings = data["level_settings"]
        self.image_settings = data["image_settings"]
        self.vfx_settings = data["vfx_settings"]
        self.sfx_settings = data["sfx_settings"]
        self.current_level = self.get_level(level)

    def get_level(self, level):
        for level in self.level_settings:
            if level["level"] == level:
                return level
        return self.level_settings[0]

    def get_level_setting(self, key):
        return self.current_level[key]

    def get_image_setting(self, key):
        return self.image_settings[0][key]

    def get_vfx_setting(self, key):
        return self.vfx_settings[0][key]

    def get_sfx_setting(self, key):
        return self.sfx_settings[0][key]


