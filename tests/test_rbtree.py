import pytest
from rbtree.rbtree import RedBlackTree
from rbtree.node import Node


def check_node_valid(bst: RedBlackTree, node: Node) -> None:
    if node.is_null():
        assert node.is_black()
        assert node.parent.is_null()
        assert node.left.is_null()
        assert node.right.is_null()
        return

    if node.is_red():
        assert node.left.is_black()
        assert node.right.is_black()

    if not node.left.is_null():
        assert node >= node.left
    if not node.right.is_null():
        assert node <= node.right


def check_valid_recur(bst: RedBlackTree, node: Node) -> int:
    check_node_valid(bst, node)

    if node.is_null():
        return 1

    if node.left.is_null() and node.right.is_null():
        if node.is_black():
            return 2
        else:
            return 1

    left_count = check_valid_recur(bst, node.left)
    right_count = check_valid_recur(bst, node.right)

    assert left_count == right_count

    # doesn't matter which one we choose because they're the same
    cur_count = left_count
    if node.is_black():
        cur_count += 1

    return cur_count


def check_valid(bst: RedBlackTree) -> None:
    root = bst.root
    assert root.is_black()
    check_valid_recur(bst, root)


def three_tree() -> RedBlackTree:
    bst = RedBlackTree()
    two = Node(2)
    bst._root = two
    two._red = False
    one = Node(1)
    one.parent = two
    two.left = one
    three = Node(3)
    three.parent = two
    two.right = three
    return bst


def test_insert() -> None:
    bst = RedBlackTree()
    assert len(bst) == 0
    bst.insert(55)
    assert len(bst) == 1
    check_valid(bst)


def test_insert_node() -> None:
    bst = RedBlackTree()
    one = Node(1)
    bst.insert(one)
    assert len(bst) == 1
    check_valid(bst)


def test_duplicate_insert() -> None:
    """
    bst will silently do nothing if adding a key that already exists
    """
    bst = RedBlackTree()
    assert len(bst) == 0
    bst.insert(55)
    bst.insert(55)
    assert len(bst) == 1


def test_search() -> None:
    bst = RedBlackTree()
    assert bst.search(60).is_null()
    bst.insert(30)
    assert bst.search(30).key == 30


def test_delete() -> None:
    bst = RedBlackTree()
    bst.insert(78)
    assert len(bst) == 1
    bst.delete(78)
    assert len(bst) == 0


def test_delete_not_exist() -> None:
    """
    bst will silently no nothing if deleteing a key that does not exist
    """
    bst = RedBlackTree()
    bst.delete(78)
    assert len(bst) == 0


def test_get_root() -> None:
    bst = RedBlackTree()
    assert bst.root.is_null()
    bst.insert(3)
    assert bst.root.key == 3


def test_rotation1() -> None:
    """
    inserting three decreasing values in a row will force a shift in the root
    node
    """
    bst = RedBlackTree()
    bst.insert(3)
    assert bst.root.key == 3
    bst.insert(2)
    bst.insert(1)
    assert bst.root.key == 2


def test_rotation2() -> None:
    """
    inserting three increasing values in a row will force a shift in the root
    node
    """
    bst = RedBlackTree()
    bst.insert(1)
    assert bst.root.key == 1
    bst.insert(2)
    bst.insert(3)
    assert bst.root.key == 2


def test_rotation3() -> None:
    """
    An inside grandchild also forces a rotation
    """
    bst = RedBlackTree()
    bst.insert(1)
    assert bst.root.key == 1
    bst.insert(3)
    bst.insert(2)
    assert bst.root.key == 2


def test_rotation4() -> None:
    """
    An inside grandchild also forces a rotation
    """
    bst = RedBlackTree()
    bst.insert(3)
    assert bst.root.key == 3
    bst.insert(1)
    bst.insert(2)
    assert bst.root.key == 2


def test_delete_rotation1() -> None:
    bst = RedBlackTree()
    one = Node(1)
    two = Node(2)
    three = Node(3)
    four = Node(4)
    bst._root = two
    two.left = one
    one.parent = two
    two.right = three
    three.parent = two
    three.right = four
    four.parent = three
    one._red = False
    two._red = False
    three._red = False
    check_valid(bst)
    bst.delete(1)
    check_valid(bst)
    assert bst.root.key == 3


def test_delete_given_node() -> None:
    bst = RedBlackTree()
    one = Node(1)
    bst._root = one
    one._red = False
    check_valid(bst)

    # Test
    bst.delete(one)
    check_valid(bst)


def test_delete_root_with_children() -> None:
    bst = three_tree()

    # Test
    bst.delete(2)
    check_valid(bst)


def test_delete_rotation2() -> None:
    bst = RedBlackTree()
    bst.insert(4)
    bst.insert(3)
    bst.insert(2)
    bst.insert(1)
    assert bst.root.key == 3
    bst.delete(4)
    assert bst.root.key == 2


def test_delete_with_right_child() -> None:
    bst = RedBlackTree()
    bst.insert(1)
    bst.insert(2)
    bst.insert(3)
    bst.insert(4)
    assert bst.root.key == 2
    bst.delete(3)
    assert bst.root.key == 2


def test_delete_with_left_child() -> None:
    bst = RedBlackTree()
    bst.insert(4)
    bst.insert(3)
    bst.insert(2)
    bst.insert(1)
    assert bst.root.key == 3
    bst.delete(2)
    assert bst.root.key == 3


def test_delete_with_grandchildren() -> None:
    bst = RedBlackTree()
    bst.insert(1)
    bst.insert(2)
    bst.insert(3)
    bst.insert(4)
    bst.delete(bst.root)
    check_valid(bst)


def test_max() -> None:
    bst = three_tree()
    assert bst.maximum().key == 3


def test_empty_max() -> None:
    bst = RedBlackTree()
    assert bst.maximum().is_null()


def test_empty_min() -> None:
    bst = RedBlackTree()
    assert bst.minimum().is_null()


def test_min() -> None:
    bst = three_tree()
    assert bst.minimum().key == 1


def test_successor() -> None:
    bst = three_tree()
    assert bst.successor(bst.root).key == 3


def test_empty_successor() -> None:
    bst = RedBlackTree()
    bst.root.parent == bst.root
    assert bst.successor(bst.root).is_null()


def test_null_right_successor() -> None:
    bst = three_tree()
    bst.insert(0)
    assert bst.successor(1).key == 2


def test_predecessor() -> None:
    bst = three_tree()
    assert bst.predecessor(bst.root).key == 1


def test_empty_predecessor() -> None:
    bst = RedBlackTree()
    assert bst.predecessor(bst.root).is_null()


def test_null_left_predecessor() -> None:
    bst = three_tree()
    bst.insert(4)
    assert bst.predecessor(3).key == 2


def test_non_int_float() -> None:
    bst = RedBlackTree()
    bst.insert(42)
    bst.insert(42.5)
    check_valid(bst)


def test_tuple() -> None:
    bst = RedBlackTree()
    bst.insert((2, 6))
    bst.insert((1, 42))
    bst.insert((1, 16))
    check_valid(bst)


def test_string() -> None:
    bst = RedBlackTree()
    bst.insert("foo")
    bst.insert("bar")
    bst.insert("Foo")
    check_valid(bst)


def test_preorder() -> None:
    bst = three_tree()
    assert len(bst.preorder()) == 3

    # There should be 4 additional Null Nodes.
    assert len(bst.preorder(True)) == 7


def test_depth() -> None:
    bst = three_tree()
    assert bst.root.depth() == 0
    assert bst.root.left.depth() == 1


def test_null_depth() -> None:
    bst = RedBlackTree()
    assert bst.root.depth() == -1


def test_iter_no_nulls() -> None:
    bst = three_tree()
    bst.use_preorder()
    bst.exclude_nulls()
    expected = [2, 1, 3]
    i = 0
    for node in bst:
        assert node.key == expected[i]
        i += 1


def test_iter_nulls() -> None:
    bst = three_tree()
    bst.include_nulls()
    expected = [2, 1, "", "", 3, "", ""]
    i = 0
    for node in bst:
        if expected[i] == "":
            assert node.is_null()
        else:
            assert node.key == expected[i]
        i += 1


def test_postorder_iter() -> None:
    bst = three_tree()
    bst.include_nulls()
    bst.use_postorder()
    expected = ["", "", 1, "", "", 3, 2]
    i = 0
    for node in bst:
        if expected[i] == "":
            assert node.is_null()
        else:
            assert node.key == expected[i]
        i += 1


def test_inorder_iter() -> None:
    bst = three_tree()
    bst.include_nulls()
    bst.use_inorder()
    expected = ["", 1, "", 2, "", 3, ""]
    i = 0
    for node in bst:
        if expected[i] == "":
            assert node.is_null()
        else:
            assert node.key == expected[i]
        i += 1


def test_to_mindmap() -> None:
    bst = three_tree()
    lat = " <latex>\\rotatebox{-90}{"
    expected = ("@startmindmap\n"
                + "-[#white]" + lat + "2}</latex>\n"
                + "--[#red]" + lat + "1}</latex>\n"
                + "---[#white]" + lat + "}</latex>\n"
                + "---[#white]" + lat + "}</latex>\n"
                + "--[#red]" + lat + "3}</latex>\n"
                + "---[#white]" + lat + "}</latex>\n"
                + "---[#white]" + lat + "}</latex>\n"
                + "@endmindmap")
    assert bst.to_mindmap() == expected


def test_str() -> None:
    bst = RedBlackTree()
    one = Node(1)
    two = Node(2)
    three = Node(3)
    four = Node(4)
    bst._root = two
    two.left = one
    one.parent = two
    two.right = three
    three.parent = two
    three.right = four
    four.parent = three
    one._red = False
    two._red = False
    three._red = False

    expected = """2(BLACK)
     L----   1(BLACK)
     R----  3(BLACK)
          R----  4(RED)
"""
    assert str(bst) == expected


def test_bad_color() -> None:
    one = Node(1)
    with pytest.raises(Exception):
        one.color = "blue"
