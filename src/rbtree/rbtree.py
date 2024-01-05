# Implementing Red-Black Tree in Python
# Adapted from https://www.programiz.com/dsa/red-black-tree

import sys
from typing import Any, Optional, TypeVar, Iterator
from rbtree.node import Node


T = TypeVar('T', bound='RedBlackTree')


class RedBlackTree():
    def __init__(self: T) -> None:
        self.root = Node()
        self.size = 0
        self._iterator_include_nulls = False

    def __iter__(self: T) -> Iterator:
        nulls = self._iterator_include_nulls
        return iter(self.preorder(nulls))

    def __getitem__(self: T, key: Any) -> Any:
        return self.search(key).value

    def __setitem__(self: T, key: Any, value: Any) -> None:
        self.search(key).value = value

    def __len__(self: T) -> int:
        return self.size

    def __str__(self: T) -> str:
        return self.__print_helper(self.root, "", 'root')

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
        if not node.is_null():
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
        if not node.is_null():
            self.in_order_helper(node.left)
            sys.stdout.write(str(node.key) + " ")
            self.in_order_helper(node.right)

    def post_order_helper(self: T, node: Node) -> None:
        """
        Create an array of child elements following
        a postorder traversal of the tree.
        """
        if not node.is_null():
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            sys.stdout.write(str(node.key) + " ")

    def preorder(self: T, include_nulls: bool = False) -> list:
        return self.pre_order_helper(self.root, include_nulls)

    def inorder(self: T) -> None:
        self.in_order_helper(self.root)

    def postorder(self: T) -> None:
        self.post_order_helper(self.root)

    # Search the tree
    def search_tree_helper(self: T, node: Node, key: Any) -> Node:
        if node.is_null() or key == node.key:
            return node

        if key < node.key:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    # Balancing the tree after deletion
    def delete_fix(self: T, x: Node) -> None:
        while x != self.root and x.is_black():
            if x == x.parent.left:
                s = x.parent.right
                if s.is_red():
                    s.set_color("black")
                    x.parent.set_color("red")
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.is_black() and s.right.is_black():
                    s.set_color("red")
                    x = x.parent
                else:
                    if s.right.is_black():
                        s.left.set_color("black")
                        s.set_color("red")
                        self.right_rotate(s)
                        s = x.parent.right

                    s.set_color(x.parent.get_color())
                    x.parent.set_color("black")
                    s.right.set_color("black")
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.is_red():
                    s.set_color("black")
                    x.parent.set_color("red")
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.is_black() and s.right.is_black():
                    s.set_color("red")
                    x = x.parent
                else:
                    if s.left.is_black():
                        s.right.set_color("black")
                        s.set_color("red")
                        self.left_rotate(s)
                        s = x.parent.left

                    s.set_color(x.parent.get_color())
                    x.parent.set_color("black")
                    s.left.set_color("black")
                    self.right_rotate(x.parent)
                    x = self.root
        x.set_color("black")

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
        z = Node()
        while not node.is_null():
            if node.key == key:
                z = node

            if node.key <= key:
                node = node.right
            else:
                node = node.left

        if z.is_null():
            # print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.get_color()
        if z.left.is_null():
            # If no left child, just scoot the right subtree up
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right.is_null():
            # If no right child, just scoot the left subtree up
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.get_color()
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
            y.set_color(z.get_color())
        if y_original_color == "black":
            self.delete_fix(x)

        self.size -= 1

    # Balance the tree after insertion
    def _fix_insert(self: T, k: Node) -> None:
        while k.parent.is_red():
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.is_red():
                    u.set_color("black")
                    k.parent.set_color("black")
                    k.parent.parent.set_color("red")
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.set_color("black")
                    k.parent.parent.set_color("red")
                    self.left_rotate(k.parent.parent)
            else:
                assert isinstance(k.parent.parent, Node)
                u = k.parent.parent.right

                if u.is_red():
                    u.set_color("black")
                    k.parent.set_color("black")
                    k.parent.parent.set_color("red")
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    l = k.parent
                    assert isinstance(l, Node)
                    l.set_color("black")
                    m = l.parent
                    assert isinstance(m, Node)
                    m.set_color("red")
                    self.right_rotate(m)
            if k == self.root:
                break
        self.root.set_color("black")

    # Printing the tree
    def __print_helper(self: T, node: Node, indent: str, last: str) -> str:
        output = ''
        if not node.is_null():
            output += indent
            if last == 'root':
                indent += "     "
            elif last == 'last':
                output += "R----  "
                indent += "     "
            else:
                output += "L----   "
                indent += "|    "

            s_color = "RED" if node.is_red() else "BLACK"
            output += str(node.key) + "(" + s_color + ")\n"
            output += self.__print_helper(node.left, indent, 'not_last')
            output += self.__print_helper(node.right, indent, 'last')
        return output

    def search(self: T, key: int) -> Node:
        """
        Find the node with the given key
        """
        return self.search_tree_helper(self.root, key)

    def minimum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node.is_null():
            return Node()
        while not node.left.is_null():
            node = node.left
        return node

    def maximum(self: T, node: Optional[Node] = None) -> Node:
        if node is None:
            node = self.root
        if node.is_null():
            return Node()
        while not node.right.is_null():
            node = node.right
        return node

    def successor(self: T, x: Node) -> Optional[Node]:
        if not x.right.is_null():
            return self.minimum(x.right)

        y = x.parent

        while y is not None and not y.is_null() and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self: T,  x: Node) -> Optional[Node]:
        if (not x.left.is_null()):
            return self.maximum(x.left)

        y = x.parent
        while y is not None and not y.is_null() and x == y.left:
            x = y
            y = y.parent

        return y

    def left_rotate(self: T, x: Node) -> None:
        y = x.right
        x.right = y.left
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
        # Allow the user to provide a custom node.
        if isinstance(key, Node):
            node = key
        else:
            node = Node(key)
        node.parent = None
        node.key = key
        node.left = Node()
        node.left.parent = node
        node.right = Node()
        node.right.parent = node
        node.set_color("red")

        y = None
        x = self.root

        while not x.is_null():
            y = x
            if node == x:
                return
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
            node.set_color("black")
            return

        if node.parent.parent is None:
            return

        self._fix_insert(node)

    def delete(self: T, key: Any) -> None:
        self.delete_node_helper(self.root, key)

    def print_tree(self: T) -> None:
        print(self.__print_helper(self.root, "", 'root'))

    def to_mindmap(self: T) -> str:
        output = "@startmindmap\n"
        for node in self.preorder(True):
            key = "" if node.key is None else node.key
            color = "white" if node.is_black() else "red"
            output += ("-" * (node.depth() + 1)
                       + "[#" + color + "] <latex>\\rotatebox{-90}{"
                       + str(key)
                       + "}</latex>\n")
        return output + "@endmindmap"
