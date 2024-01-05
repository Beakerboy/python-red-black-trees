from typing import Any, TypeVar


T = TypeVar('T', bound='Node')


class Node():

    def __init__(self: T, key: Any = None) -> None:
        self.key = key
        self.parent: Node | None = None
        self.left: Node
        self.right: Node
        self._color = 0 if key is None else 1
        self.value: Any = None

    def __repr__(self: T) -> str:
        return "Key: " + str(self.key) + " Value: " + str(self.value)

    def __lt__(self: T, other: Any) -> bool:
        return self.key < other.key

    def __le__(self: T, other: Any) -> bool:
        return self.key <= other.key

    def __gt__(self: T, other: Any) -> bool:
        return self.key > other.key

    def __ge__(self: T, other: Any) -> bool:
        return self.key >= other.key

    def __eq__(self: T, other: Any) -> bool:
        return self.key == other.key

    def __ne__(self: T, other: Any) -> bool:
        return self.key != other.key

    def get_color(self: T) -> str:
        return "black" if self._color == 0 else "red"

    def set_color(self: T, color: str) -> None:
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
        return self.key is None

    def depth(self: T) -> int:
        return 0 if self.parent is None else self.parent.depth() + 1
