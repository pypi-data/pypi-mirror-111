import threading
import typing as t
from abc import ABCMeta, abstractmethod


class Observable(object):
    def __init__(self) -> None:
        super().__init__()
        self.__observers: t.List["Observer"] = []

    def register_observer(
        self, observer: "Observer"
    ) -> None:
        self.__observers.append(observer)

    def remove_observer(
        self, observer: "Observer"
    ) -> None:
        if observer in self.__observers:
            del self.__observers[observer]

    def notify_observers(self, name: str, *args, **kwargs) -> None:
        for observer in self.__observers:
            observer.handle_notification(
                name, *args, **kwargs)


class Observer(metaclass=ABCMeta):
    @abstractmethod
    def handle_notification(self, name: str, *args, **kwargs) -> None:
        pass


class Singleton(object):
    """ Thread safe Singleton"""
    __instance__ = None
    _lock = threading.Lock()

    @classmethod
    def initialized(cls) -> bool:
        return cls.__instance__ is not None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        with cls._lock:
            if not cls.__instance__:
                cls.__instance__ = cls(*args, **kwargs)
            
            return cls.__instance__
