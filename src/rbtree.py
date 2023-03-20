# Implementing Red-Black Tree in Python
# Adapted from https://www.programiz.com/dsa/red-black-tree

import sys
from typing import TypeVar, Any, Iterator


T = TypeVar('T', bound='Node')


# Node creation
class Node():

    def __init__(self: T, key: Any) -> None:
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1
        self.value = None

    def __repr__(self: T) -> str:
        return "Key: " + str(self.key) + " Value: " + str(self.value)

    def __lt__(self: T, other: T) -> bool:
        return self.key < other.key

    def __le__(self: T, other: T) -> bool:
        return self.key <= other.key

    def __gt__(self: T, other: T) -> bool:
        return self.key > other.key

    def __ge__(self: T, other: T) -> bool:
        return self.key >= other.key

    def __eq__(self: T, other: T) -> bool:
        return self.key == other.key

    def __ne__(self: T, other: T) -> bool:
        return self.key != other.key

    def is_red(self: T) -> bool:
        return self.color == 1

    def is_black(self: T) -> bool:
        return self.color == 0

    def depth(self: T) -> int:
        return 0 if self.parent is None else self.parent.depth() + 1


T = TypeVar('T', bound='RedBlackTree')


class RedBlackTree():
    def __init__(self: T) -> None:
        self.TNULL = Node(0)
        self.TNULL.id = -1
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.size = 0
        self._iterator_include_nulls = False

    def __iter__(self: T) -> Iterator:
        nulls = self._iterator_include_nulls
        return iter(self.preorder(nulls))

    def __getitem__(self: T, key: Any) -> Any:
        return self.search(key).value

    def __setitem__(self: T, key: Any, value: Any) -> None:
        self.search(key).value = value

    # Getters and Setters
    def get_root(self: T) -> Node:
        return self.root

    def pre_order_helper(self: T,
                         node: Node,
                         include_nulls: bool = False) -> list:
        """
        Create an array of child elements following
        a preorder traversal of the tree.
        """
        left = []
        right = []
        basenode = []
        if node != self.TNULL:
            basenode = [node]
            left = self.pre_order_helper(node.left, include_nulls)
            right = self.pre_order_helper(node.right, include_nulls)
        if include_nulls:
            basenode = [node]
        basenode.extend(left)
        basenode.extend(right)
        return basenode

    def in_order_helper(self: T, node: Node) -> None:
        """
        Create an array of child elements following
        a inorder traversal of the tree.
        """
        if node != self.TNULL:
            self.in_order_helper(node.left)
            sys.stdout.write(str(node.key) + " ")
            self.in_order_helper(node.right)

    def post_order_helper(self: T, node: Node) -> None:
        """
        Create an array of child elements following
        a postorder traversal of the tree.
        """
        if node != self.TNULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            sys.stdout.write(str(node.key) + " ")

    def preorder(self: T, include_nulls: bool = False) -> list:
        return self.pre_order_helper(self.root, include_nulls)

    def inorder(self: T) -> list:
        self.in_order_helper(self.root)

    def postorder(self: T) -> None:
        self.post_order_helper(self.root)

    # Search the tree
    def search_tree_helper(self: T, node: Node, key: Any) -> Node:
        if node == self.TNULL or key == node.key:
            return node

        if key < node.key:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    # Balancing the tree after deletion
    def delete_fix(self: T, x: Node) -> None:
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def __rb_transplant(self: T, u: Node, v: Node) -> None:
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Node deletion
    def delete_node_helper(self: T, node: Node, key: int) -> None:
        z = self.TNULL
        while node != self.TNULL:
            if node.key == key:
                z = node

            if node.key <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            # print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            # If no left child, just scoot the right subtree up
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            # If no right child, just scoot the left subtree up
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.delete_fix(x)

        self.size -= 1

    # Balance the tree after insertion
    def fix_insert(self: T, k: Node) -> None:
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    # Printing the tree
    def __print_helper(self: T, node: Node, indent: str, last: bool) -> None:
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----  ")
                indent += "     "
            else:
                sys.stdout.write("L----   ")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.key) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def search(self: T, key: int) -> Node:
        """
        Find the node with the given key
        """
        return self.search_tree_helper(self.root, key)

    def minimum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node == self.TNULL:
            return self.TNULL
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node == self.TNULL:
            return self.TNULL
        while node.right != self.TNULL:
            node = node.right
        return node

    def successor(self: T, x: Node) -> Node:
        if x.right != self.TNULL:
            return self.minimum(x.right)

        y = x.parent
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self: T,  x: Node) -> Node:
        if (x.left != self.TNULL):
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent

        return y

    def left_rotate(self: T, x: Node) -> None:
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self: T, x: Node) -> None:
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self: T, key: Any) -> None:
        node = Node(key)
        node.parent = None
        node.key = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node < x:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node < y:
            y.left = node
        else:
            y.right = node

        self.size += 1

        if node.parent is None:
            node.color = 0
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def delete(self: T, key: Any) -> None:
        self.delete_node_helper(self.root, key)

    def print_tree(self: T) -> None:
        self.__print_helper(self.root, "", True)

    def to_mindmap(self: T) -> str:
        original = self._iterator_include_nulls
        self._iterator_include_nulls = True
        output = "@startmindmap\n"
        for node in self:
            color = "white" if node.color == 0 else "red"
            output += ("-" * (node.depth() + 1)
                       + "[#" + color + "] <latex>\\rotatebox{-90}{"
                       + str(node.key)
                       + "}</latex>\n")
        self._iterator_include_nulls = original
        return output + "@endmindmap"
