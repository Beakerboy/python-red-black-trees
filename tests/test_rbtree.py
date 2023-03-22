from rbtree import RedBlackTree, Node


def check_node_valid(bst: RedBlackTree, node: Node) -> None:
    if node.is_null():
        assert node.is_black()
        return

    if node.is_red():
        assert node.left.is_black()
        assert node.right.is_black()

    if not node.left.is_null() and node.left is not None:
        assert node >= node.left
    if not node.right.is_null() and node.right is not None:
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
    root = bst.get_root()
    assert root.is_black()

    check_valid_recur(bst, root)


def test_insert() -> None:
    bst = RedBlackTree()
    bst.insert(55)
    assert bst.search(55).key == 55
    bst.insert(40)
    assert bst.search(40).key == 40
    bst.insert(58)
    assert bst.search(58).key == 58
    bst.insert(42)
    assert bst.search(42).key == 42

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

    assert bst.size == 17

    check_valid(bst)


def test_search() -> None:
    bst = RedBlackTree()
    assert bst.search(60).is_null()
    bst.insert(30)
    assert bst.search(30).key == 30


def test_delete() -> None:
    bst = RedBlackTree()
    bst.insert(78)
    assert bst.search(78).key == 78
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

    assert bst.size == 7

    bst.delete(48)
    assert bst.size == 6
    bst.delete(42)
    assert bst.size == 5
    bst.delete(42)
    assert bst.size == 5
    assert bst.search(42).is_null()
    assert bst.size == 5
    bst.delete(100)
    assert bst.size == 4

    bst.delete(100)

    assert bst.size == 4
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
    assert bst.get_root().key == 3


def test_accessors() -> None:
    bst = RedBlackTree()
    assert bst.maximum().is_null()
    assert bst.minimum().is_null()

    bst.insert(55)
    bst.insert(40)
    bst.insert(58)
    bst.insert(42)

    assert bst.maximum().key == 58
    assert bst.minimum().key == 40
    assert bst.successor(bst.search(42)).key == 55
    assert bst.successor(bst.search(40)).key == 42
    assert bst.successor(bst.search(55)).key == 58
    assert bst.predecessor(bst.search(42)).key == 40
    assert bst.predecessor(bst.search(55)).key == 42
    assert bst.predecessor(bst.search(58)).key == 55

    bst.insert(57)
    assert bst.predecessor(bst.search(57)).key == 55


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


def tes_duplicates() -> None:
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
    bst = RedBlackTree()
    bst.insert(1)
    bst.insert(3)
    bst.insert(2)
    assert len(bst.preorder()) == 3

    # There should be 4 additional Null Nodes.
    assert len(bst.preorder(True)) == 7


def test_null_depth() -> None:
    bst = RedBlackTree()
    bst.insert(1)
    bst.insert(3)
    bst.insert(2)
    nodes = bst.preorder(True)
    assert nodes[0].key == 2
    assert nodes[0].depth() == 0
    assert nodes[1].key == 1
    assert nodes[1].depth() == 1
    assert nodes[2].key is None
    assert nodes[2].depth() == 2
    assert nodes[3].key is None
    assert nodes[3].depth() == 2
    assert nodes[4].key == 3
    assert nodes[4].depth() == 1
    assert nodes[5].key is None
    assert nodes[5].depth() == 2
    assert nodes[6].key is None
    assert nodes[6].depth() == 2


def test_to_mindmap() -> None:
    bst = RedBlackTree()
    bst.insert(1)
    bst.insert(3)
    bst.insert(2)
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
