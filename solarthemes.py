import configparser

config = configparser.ConfigParser()

class Themes():
    def __init__(self, theme):
        self.theme = theme

    def ThemeInfo(self):
        with open("themes.solar", "r") as configfile:
            config.read_file(configfile)
            bgdefault = config[self.theme]["background"]
            fgdefault = config[self.theme]["foreground"]
            ttktheme = config[self.theme]["ttktheme"]
            return ttktheme, bgdefault, fgdefault
