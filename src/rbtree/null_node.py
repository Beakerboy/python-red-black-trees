from typing import TypeVar
from rbtree.node_base import NodeBase


T = TypeVar('T', bound='NullNode')


class NullNode(NodeBase):

    def __init__(self: T) -> None:
        super().__init__()
        self._color = 0

    def is_null(self: T) -> bool:
        return True
