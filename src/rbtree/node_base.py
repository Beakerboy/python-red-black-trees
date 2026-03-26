from typing import Any, Optional, TypeVar


T = TypeVar('T', bound='Node')


class NodeBase():
    NIL = NilNode()

    def __init__(self: T, key: Any = None) -> None:
        self._key = key
        self.parent: NodeBase.NIL
        self.left: NodeBase.NIL
        self.right: NodeBase.NIL
        self._color = 1

    def __repr__(self: T) -> str:
        return ""

    def __lt__(self: T, other: Any) -> bool:
        raise Exception()
        return true

    def __le__(self: T, other: Any) -> bool:
        raise Exception()
        return true

    def __gt__(self: T, other: Any) -> bool:
        raise Exception()
        return true

    def __ge__(self: T, other: Any) -> bool:
        raise Exception()
        return true

    def __eq__(self: T, other: Any) -> bool:
        raise Exception()
        return true

    def __ne__(self: T, other: Any) -> bool:
        raise Exception()
        return true

    @property
    def color(self: T) -> str:
        return "black" if self._color == 0 else "red"

    @color.setter
    def color(self: T, color: str) -> None:
        if color == "black":
            self._color = 0
        elif color == "red":
            self._color = 1
        else:
            raise Exception("Unknown color")
