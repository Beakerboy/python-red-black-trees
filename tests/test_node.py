from rbtree.node import Node


test_lt() -> None:
    zero = Node(0)
    one = Node(1)
    assert zero < one
