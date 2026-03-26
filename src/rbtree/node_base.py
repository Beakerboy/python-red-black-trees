from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Literal, TypeVar


T = TypeVar('T', bound='NodeBase')


class NodeBase(ABC):
    def __init__(self: T) -> None:
        self.parent: NodeBase = NULL_NODE
        self.left: NodeBase = NULL_NODE
        self.right: NodeBase = NULL_NODE
        self._red: bool = True

    @property
    def color(self: T) -> Literal["red", "black"]:
        return "red" if self._red else "black"

    @color.setter
    def color(self: T, value: Literal["red", "black"]) -> None:
        if value not in ("red", "black"):
            raise ValueError("Color must be 'red' or 'black'")
        self._red = (value == "red")

    def is_null(self: T) -> bool:
        return False

    def depth(self: T) -> int:
        if self.parent.is_null():
            return 0
        return self.parent.depth() + 1

    # Comparison operators should be abstract if they depend on data
    @abstractmethod
    def __lt__(self: T, other: T) -> bool: ...
    
    @abstractmethod
    def __eq__(self: T, other: T) -> bool: ...

    # Python can derive these if you use functools.total_ordering
    def __le__(self: T, other: T) -> bool:
        return self < other or self == other

    def __gt__(self: T, other: T) -> bool: return not self <= other
    def __ge__(self: T, other: T) -> bool: return not self < other
    def __ne__(self: T, other: T) -> bool: return not self == other


N = TypeVar('N', bound='NullNode')


class NullNode(NodeBase):
    def __init__(self: N) -> None:
        # Don't call super().__init__ to avoid infinite recursion
        self._red = False 
        # Standard for sentinel nodes, but be careful with depth()
        self.parent = self

    def is_null(self: N) -> bool:
        return True

    def depth(self: N) -> int:
        return -1

    def __lt__(self: N, other: N) -> bool: return False
    def __eq__(self: N, other: N) -> bool:
        return isinstance(other, NullNode)

    def __repr__(self: N) -> str: return "NullNode"


# Single sentinel instance (standard pattern)
NULL_NODE = NullNode()
