import os
from configparser import ConfigParser


class Config(dict):
    def __init__(self):
        super().__init__()

        self.__associate = False

    def from_ini(self, file: str, associate=False) -> None:
        if not os.path.exists(file):
            raise RuntimeError(
                    f"Could not find config file {file}")

        cf_p = ConfigParser()
        cf_p.read(file)

        self.__associate = associate

        for section in cf_p.sections():
            for key, val in cf_p.items(section):
                if associate:
                    if not section in self:
                        self[section] = {}
                    self[section][key] = val
                else:
                    self[key] = val

    def has_option(
        self,
        option: str, section: str = 'default'
    ) -> bool:
        try:
            v = None
            if self.__associate:
                v = self[section][option]
            else:
                v = self[option]
            return v is not None
        except KeyError:
            return False
