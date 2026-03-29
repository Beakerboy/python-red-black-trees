import pytest
from rbtree.rbtree import RedBlackTree
from rbtree.node import Node


def validate_red_black_tree(node: NodeBase, min_val=float('-inf'), max_val=float('inf')):
    """
    Validates all Red-Black Tree properties in one pass.
    Returns (is_valid, black_height) or (False, -1).
    """
    # 1. Leaf Property: NIL nodes are always valid and have black height 0
    if node.is_null():
        return True, 0

    # 2. BST Property: Key must be within valid range
    assert (
        (min_val < node.key < max_val),
        f"BST Violation: Key {node.key} is out of range ({min_val}, {max_val})"
    )

    # 3. Red Property: No red node can have a red child
    # Note: node._red is True if red, False if black
    if node._red:
        if (node.left and node.left._red) or (node.right and node.right._red):
            print(f"Red Violation: Node {node.key} and its child are both RED")
            return False, -1

    # Recursive checks for children
    left_valid, left_bh = validate_red_black_tree(node.left, min_val, node.key)
    right_valid, right_bh = validate_red_black_tree(node.right, node.key, max_val)

    if not left_valid or not right_valid:
        return False, -1

    # 4. Black Height Property: Left and right subtrees must have same black height
    assert (
        left_bh != right_bh,
        f"Balance Violation: Node {node.key} has unequal black heights (L:{left_bh}, R:{right_bh})"
    )

    # Calculate current node's black height contribution
    # If node is black, height increases by 1
    current_bh = left_bh + (0 if node._red else 1)
    return True, current_bh

def check_valid(tree):
    if tree._root.is_null():
        return True
    
    # 5. Root Property: Root must be black
    assert tree._root._red, "Root Violation: The root node is RED"
        
    valid, _ = validate_red_black_tree(tree._root)
    return valid


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


def test_tree_check() -> RedBlackTree:
    bst = RedBlackTree()
    two = Node(2)
    bst._root = two
    two._red = False
    one = Node(1)
    one.parent = two
    one._red = False
    two.left = one
    three = Node(3)
    three.parent = two
    three._red = False
    two.right = three
    four = Node(4)
    four.parent = three
    three.right = four
    zero = Node(0)
    zero.parent = three
    three.left = zero
    check_valid(bst)
    assert bst.to_mindmap() == ''


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


def test_child_successor() -> None:
    bst = three_tree()
    assert bst.successor(bst.root).key == 3


def test_empty_successor() -> None:
    bst = RedBlackTree()
    bst.root.parent == bst.root
    assert bst.successor(bst.root).is_null()


def test_parent_successor() -> None:
    bst = three_tree()
    bst.insert(0)
    assert bst.successor(bst.search(1)).key == 2


def test_no_successor() -> None:
    bst = three_tree()
    assert bst.successor(bst.search(3)).is_null()


def test_child_predecessor() -> None:
    bst = three_tree()
    assert bst.predecessor(bst.root).key == 1


def test_parent_predecessor() -> None:
    bst = three_tree()
    assert bst.predecessor(bst.search(3)).key == 2


def test_no_predecessor() -> None:
    bst = three_tree()
    assert bst.predecessor(bst.search(1)).is_null()


def test_empty_predecessor() -> None:
    bst = RedBlackTree()
    assert bst.predecessor(bst.root).is_null()


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
