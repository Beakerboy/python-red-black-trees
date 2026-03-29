from rbtree.node import Node


def test_lt() -> None:
    zero = Node(0)
    one = Node(1)
    assert zero < one


def test_str() -> None:
    zero = Node(0)
    assert str(zero) == "0"


def test_repr() -> None:
    zero = Node(0)
    assert repr(zero) == "Key: 0"
