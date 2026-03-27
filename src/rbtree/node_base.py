from typing import Any, TypeVar


T = TypeVar('T', bound='NodeBase')


class NodeBase():
    NIL: 'NullNode'

    def __init__(self: T) -> None:
        self.parent: NodeBase = NodeBase.NIL
        self.left: NodeBase = NodeBase.NIL
        self.right: NodeBase = NodeBase.NIL
        self._red = True

    def __repr__(self: T) -> str:
        return ""

    def __str__(self: T) -> str:
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
        return "black" if not self._red else "red"

    @color.setter
    def color(self: T, color: str) -> None:
        if color == "black":
            self._red = False
        elif color == "red":
            self._red = True
        else:
            raise Exception("Unknown color")

    def is_red(self: T) -> bool:
        return self._red

    def is_black(self: T) -> bool:
        return not self._red

    def is_null(self: T) -> bool:
        return False

    def depth(self: T) -> int:
        return 0 if self.parent.is_null() else self.parent.depth() + 1


N = TypeVar('N', bound='NullNode')


class NullNode(NodeBase):

    def __init__(self: N) -> None:
        self.parent = self
        self.left = self
        self.right = self
        self._red = False

    def is_null(self: N) -> bool:
        return True

    def __eq__(self: T, other: Any) -> bool:
        return other.is_null()

    def __ne__(self: T, other: Any) -> bool:
        return not other.is_null()


NodeBase.NIL = NullNode()
