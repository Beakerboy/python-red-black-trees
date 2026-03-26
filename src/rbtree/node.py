from typing import Any, TypeVar
from rbtree.node_base import NodeBase

T = TypeVar('T', bound='Node')


class Node(NodeBase):
    """
    This node can work with any python primative type
    that can be compared with comparison operators.
    """

    def __init__(self: T, key: Any = None) -> None:
        super().__init__()
        self._key = key

    def __repr__(self: T) -> str:
        return "Key: " + str(self.key) + " Value: " + str(self.value)

    def __str__(self: T) -> str:
        return str(self._key)

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

    @property
    def key(self: T) -> Any:
        return self._key
