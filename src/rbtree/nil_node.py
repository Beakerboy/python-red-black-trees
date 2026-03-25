from typing import Any, TypeVar


T = TypeVar('T', bound='Node')


class NullNode(NodeBase):

    def __init__(self: T, key: Any = None) -> None:
        self._color = 0

    def is_null(self: T) -> bool:
        return False
