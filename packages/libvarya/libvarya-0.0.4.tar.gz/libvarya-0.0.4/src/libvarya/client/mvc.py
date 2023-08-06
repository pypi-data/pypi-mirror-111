import typing as t
from abc import ABC, abstractmethod
from .patterns import Observable, Observer


class Proxy(Observable):
    pass


class ViewMixin(ABC):
    @abstractmethod
    def parent(self) -> t.Optional[t.Any]:
        pass


class Controller(Observer):
    def __init__(self, view: "ViewMixin") -> None:
        self.__parent = None
        if hasattr(view.parent(), 'controller'):
            self.__parent = view.parent().controller

        self.__subscribers: t.Dict[str, t.Callable] = {}

    @property
    def parent(self) -> "Controller":
        return self.__parent

    def subscribe(
        self, event: str, callback: t.Callable
    ) -> None:
        if callable(callback):
            self.__subscribers[event] = callback

    def handle_notification(self, 
        name:str, *args, **kwargs
    ) -> None:
        """ Chain of responsibility method """
        if name in self.__subscribers:
            callback: t.Callable = self.__subscribers[name]
            callback(*args, **kwargs)
        elif self.parent:
            self.parent.handle_notification(
                name, *args, **kwargs)

