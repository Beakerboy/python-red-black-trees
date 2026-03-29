from functools import total_ordering
from typing import Any, TypeVar
from rbtree.node_base import NodeBase

T = TypeVar('T', bound='Node')

@total_ordering
class Node(NodeBase):
    """
    This node can work with any python primative type
    that can be compared with comparison operators.
    """

    def __init__(self: T, key: Any = None) -> None:
        super().__init__()
        self._key = key

    def __repr__(self: T) -> str:
        return "Key: " + str(self.key)

    def __str__(self: T) -> str:
        return str(self._key)

    def __lt__(self: T, other: Any) -> bool:
        return self.key < other.key

    def __eq__(self: T, other: Any) -> bool:
        return not other.is_null() and self.key == other.key


    @property
    def key(self: T) -> Any:
        return self._key
