from typing import Any, TypeVar
from rbtree.null_node import NullNode


T = TypeVar('T', bound='NodeBase')


class NodeBase():
    NIL = NullNode()

    def __init__(self: T) -> None:
        self.parent = NodeBase.NIL
        self.left = NodeBase.NIL
        self.right = NodeBase.NIL
        self._color = 1

    def __repr__(self: T) -> str:
        return ""

    def __lt__(self: T, other: Any) -> bool:
        raise Exception()
        return True

    def __le__(self: T, other: Any) -> bool:
        raise Exception()
        return True

    def __gt__(self: T, other: Any) -> bool:
        raise Exception()
        return True

    def __ge__(self: T, other: Any) -> bool:
        raise Exception()
        return True

    def __eq__(self: T, other: Any) -> bool:
        raise Exception()
        return True

    def __ne__(self: T, other: Any) -> bool:
        raise Exception()
        return True

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

    def is_red(self: T) -> bool:
        return self._color == 1

    def is_black(self: T) -> bool:
        return self._color == 0

    def is_null(self: T) -> bool:
        return False

    def depth(self: T) -> int:
        return 0 if self.parent is None else self.parent.depth() + 1
