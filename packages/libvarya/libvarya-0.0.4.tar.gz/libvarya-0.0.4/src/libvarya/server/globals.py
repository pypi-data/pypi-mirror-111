import typing as t
from libvarya.common import ObjectProxy

if t.TYPE_CHECKING:
    from .app import Server


def _find_app() -> "Server":
    if len(_app_stack):
        return _app_stack[0]
    else:
        raise RuntimeError("Could not find application")


_app_stack = []
current_app: "Server" = ObjectProxy(_find_app)