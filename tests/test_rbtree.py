from rbtree import RedBlackTree, Node


def check_node_valid(bst: RedBlackTree, node: Node) -> None:
    if node.is_null():
        assert node.is_black()
        return

    if node.is_red():
        assert node.left.is_black()
        assert node.right.is_black()

    if not node.left.is_null() and node.left is not None:
        assert node.item >= node.left.item
    if not node.right.is_null() and node.right is not None:
        assert node.item <= node.right.item


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
    root = bst.get_root()
    assert root.is_black()

    check_valid_recur(bst, root)


def test_insert() -> None:
    bst = RedBlackTree()
    bst.insert(55)
    assert bst.search(55).item == 55
    bst.insert(40)
    assert bst.search(40).item == 40
    bst.insert(58)
    assert bst.search(58).item == 58
    bst.insert(42)
    assert bst.search(42).item == 42

    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(43)
    bst.insert(44)
    bst.insert(40)
    bst.insert(-10)
    bst.insert(10)
    bst.insert(15)
    bst.insert(11)
    bst.insert(100)
    bst.insert(101)
    bst.insert(103)
    bst.insert(106)
    bst.insert(107)
    bst.insert(109)
    bst.insert(102)

    assert bst.size == 23

    check_valid(bst)


def test_search() -> None:
    bst = RedBlackTree()
    assert bst.search(60).is_null()
    bst.insert(30)
    assert bst.search(30).item == 30


def test_delete() -> None:
    bst = RedBlackTree()
    bst.insert(78)
    assert bst.search(78).item == 78
    bst.delete(78)
    assert bst.search(78).is_null()

    bst.insert(73)
    bst.insert(48)
    bst.insert(100)
    bst.insert(42)
    bst.insert(55)
    bst.insert(40)
    bst.insert(58)
    bst.insert(42)
    bst.insert(55)
    bst.insert(40)
    bst.insert(58)
    bst.insert(42)

    assert bst.size == 12

    bst.delete(48)
    assert bst.size == 11
    bst.delete(42)
    assert bst.size == 10
    bst.delete(42)
    assert bst.size == 9
    assert bst.search(42).item == 42
    bst.delete(42)
    assert bst.search(42).is_null()
    assert bst.size == 8
    bst.delete(100)
    assert bst.size == 7

    bst.delete(100)

    assert bst.size == 7
    check_valid(bst)


def test_complex_delete() -> None:
    bst = RedBlackTree()

    with open("tests/small_input.txt") as infile:
        for line in infile:
            sline = line.split()
            if sline[0] == "a":
                bst.insert(int(sline[1]))
            else:
                bst.delete(int(sline[1]))
            check_valid(bst)


# def test_long() -> None:
#    bst = RedBlackTree()
#    with open("tests/test_input.txt") as infile:
#        for line in infile:
#            sline = line.split()
#            if sline[0] == "a":
#                bst.insert(int(sline[1]))
#            else:
#                bst.delete(int(sline[1]))
#            check_valid(bst)


def test_dictionary() -> None:
    bst = RedBlackTree()
    bst[67] = 3
    assert bst[67] == 3


def test_get_root() -> None:
    bst = RedBlackTree()
    assert bst.get_root().is_null()
    bst.insert(3)
    assert bst.get_root().item == 3


def test_accessors() -> None:
    bst = RedBlackTree()
    assert bst.maximum().is_null()
    assert bst.minimum().is_null()

    bst.insert(55)
    bst.insert(40)
    bst.insert(58)
    bst.insert(42)

    assert bst.maximum().item == 58
    assert bst.minimum().item == 40
    assert bst.successor(bst.search(42)).item == 55
    assert bst.successor(bst.search(40)).item == 42
    assert bst.successor(bst.search(55)).item == 58
    assert bst.predecessor(bst.search(42)).item == 40
    assert bst.predecessor(bst.search(55)).item == 42
    assert bst.predecessor(bst.search(58)).item == 55

    bst.insert(57)
    assert bst.predecessor(bst.search(57)).item == 55


def test_preorder() -> None:
    bst = RedBlackTree()
    bst.insert(1)
    bst.insert(2)
    bst.insert(3)

    pre = bst.preorder()
    keys = []
    for node in pre:
        keys.append(str(node.get_key()))
    assert " ".join(keys) == "1 2 3"


def test_print() -> None:
    bst = RedBlackTree()
    bst.insert(73)
    print(bst.get_root())
    bst.insert(48)
    bst.insert(100)
    bst.insert(42)
    bst.insert(55)
    bst.insert(40)
    bst.insert(58)
    bst.insert(42)
    bst.insert(55)
    bst.insert(40)
    bst.insert(58)
    bst.insert(42)

    bst.print_tree()
    bst.preorder()
    bst.inorder()
    bst.postorder()


def test_elaborate_delete() -> None:
    bst = RedBlackTree()
    bst.insert(55)
    bst.insert(40)
    bst.insert(58)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(43)
    bst.insert(44)
    bst.insert(40)
    bst.insert(-10)
    bst.insert(10)
    bst.insert(15)
    bst.insert(11)
    bst.insert(100)
    bst.insert(101)
    bst.insert(103)
    bst.insert(106)
    bst.insert(107)
    bst.insert(109)
    bst.insert(102)

    bst.delete(15)
    bst.delete(55)
    bst.delete(103)
    bst.delete(106)
    bst.delete(107)
    bst.delete(101)
    bst.delete(42)
    bst.delete(42)
    bst.delete(42)
    bst.delete(10)
    bst.delete(40)
    bst.delete(58)
    bst.delete(100)
    bst.delete(42)

    bst.print_tree()
    check_valid(bst)


def test_duplicates() -> None:
    bst = RedBlackTree()
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)
    bst.insert(42)

    bst.delete(42)
    bst.delete(42)
    bst.delete(42)
    bst.delete(42)
    bst.delete(42)
    bst.delete(42)
    bst.delete(42)
    check_valid(bst)
