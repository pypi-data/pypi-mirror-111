from .globals import _app_stack
from libvarya.utils import Config


class Client(object):
    def __init__(self) -> None:
        self.__config = Config()

        # set Application instance to local context
        _app_stack.append(self)

    @property
    def config(self) -> "Config":
        return self.__config
