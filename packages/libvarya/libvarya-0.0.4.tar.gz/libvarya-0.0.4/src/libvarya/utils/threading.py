import functools
import threading
from typing import Callable


class ThreadMethod(object):
    def __init__(self, func) -> None:
        super().__init__()
        self.__func: Callable = func

    def __call__(self, instance, *args, **kwargs):
        def target():
            return self.__func(instance, *args, **kwargs)

        t = threading.Thread(target=target)
        t.start()

    def __get__(self, instance, owner):
        return functools.partial(self, instance)
