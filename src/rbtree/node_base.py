from typing import Any, Literal, TypeVar
from abc import ABC, abstractmethod


T = TypeVar('T', bound='NodeBase')


class NodeBase(ABC):
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

    @abstractmethod
    def __lt__(self: T, other: Any) -> bool: ...

    @abstractmethod
    def __eq__(self: T, other: Any) -> bool: ...

    @property
    def color(self: T) -> Literal["red", "black"]:
        return "red" if self._red else "black"

    @color.setter
    def color(self: T, value: Literal["red", "black"]) -> None:
        if value not in ("red", "black"):
            raise ValueError("Color must be 'red' or 'black'")
        self._red = (value == "red")

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
        self._parent = self
        self.left = self
        self.right = self
        self._red = False

    @property
    def parent(self: N) -> NullNode:
        return self._parent

    @parent.setter
    def parent(self: N, node: NodeBase) -> None:
        raise Exeception("Cannot Change Null Node Parent")

    def __eq__(self: T, other: Any) -> bool: return other.is_null()
    def __ne__(self: T, other: Any) -> bool: return not other.is_null()
    def __lt__(self: T, other: Any) -> bool: return False

    def is_null(self: N) -> bool: return True
    def depth(self: N) -> int: return -1


NodeBase.NIL = NullNode()
