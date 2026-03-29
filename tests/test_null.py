from rbtree.node_base import NullNode

def test_null_parent() -> None:
    null = NullNode()

    with pytest.raises(Exception):
        null.parent = null


def test_null_left() -> None:
    null = NullNode()

    with pytest.raises(Exception):
        null.left = null


def test_null_right() -> None:
    null = NullNode()

    with pytest.raises(Exception):
        null.right = null
