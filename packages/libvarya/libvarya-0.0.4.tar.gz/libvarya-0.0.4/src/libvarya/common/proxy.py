import typing as t


class ObjectProxy:
    def __init__(self, lookup: t.Callable) -> None:
        super().__init__()

        object.__setattr__(self, "_lookup_callable", lookup)

    def __getattr__(self, name: str) -> t.Any:
        obj = self._get_current_object()

        if hasattr(obj, name):
            return object.__getattribute__(obj, name)

        raise RuntimeError(f"Attribute {name} not found")

    def __setattr__(self, name: str) -> t.Any:
        obj = self._get_current_object()

        if hasattr(obj, name):
            return object.__setattr__(obj, name)

        raise RuntimeError(f"Attribute {name} not found")

    def _get_current_object(self) -> t.Any:
        if hasattr(self, "_lookup_callable"):
            call_ = getattr(self, "_lookup_callable")
            return call_()

        raise RuntimeError(f"no object bound to {self}")
