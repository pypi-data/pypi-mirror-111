import typing as t
from libvarya.common import ObjectProxy

if t.TYPE_CHECKING:
    from .app import Client


def _find_app() -> "Client":
    if len(_app_stack):
        return _app_stack[0]
    else:
        raise RuntimeError("Could not find application")


_app_stack = []
current_app: "Client" = ObjectProxy(_find_app)