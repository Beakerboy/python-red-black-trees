from typing import Any, Optional, TypeVar, Iterator
from rbtree.node import Node
from rbtree.node_base import NodeBase


T = TypeVar('T', bound='RedBlackTree')


class RedBlackTree():
    def __init__(self: T) -> None:
        self.root: NodeBase = NodeBase.NIL
        self.size = 0
        self._iterator_include_nulls = False

    # Dunder Methods

    def __iter__(self: T) -> Iterator:
        nulls = self._iterator_include_nulls
        return iter(self.preorder(nulls))

    def __len__(self: T) -> int:
        return self.size

    def __str__(self: T) -> str:
        return self.__print_helper(self.root, "", 'root')

    # Getters and Setters and Properties

    def get_root(self: T) -> NodeBase:
        return self.root

    # Public Methods

    def preorder(self: T, include_nulls: bool = False) -> list:
        return self._pre_order_helper(self.root, include_nulls)

    def inorder(self: T) -> None:
        self._in_order_helper(self.root)

    def postorder(self: T) -> None:
        self._post_order_helper(self.root)

    def search(self: T, key: Any) -> NodeBase:
        """
        Find the node with the given key
        """
        return self._search_tree_helper(self.root, key)

    def minimum(self: T, node: Optional[NodeBase] = None) -> NodeBase:
        if node is None:
            node = self.root
        if node.is_null():
            return node
        while not node.left.is_null():
            node = node.left
        return node

    def maximum(self: T, node: Optional[NodeBase] = None) -> NodeBase:
        if node is None:
            node = self.root
        if node.is_null():
            return Node()
        while not node.right.is_null():
            node = node.right
        return node

    def successor(self: T, x: NodeBase) -> Optional[NodeBase]:
        if not x.right.is_null():
            return self.minimum(x.right)

        y = x.parent

        while not y.is_null() and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self: T,  x: NodeBase) -> Optional[Node]:
        if (not x.left.is_null()):
            return self.maximum(x.left)

        y = x.parent
        while not y.is_null() and x == y.left:
            x = y
            y = y.parent

        return y

    def insert(self: T, key: Any) -> None:
        # Allow the user to provide a custom node.
        if isinstance(key, NodeBase):
            node = key
        else:
            node = Node(key)
        y = NodeBase.NIL
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
        if y.is_null():
            self.root = node
        elif node < y:
            y.left = node
        else:
            y.right = node

        self.size += 1

        if node.parent.is_null():
            node.color = "black"
            return

        if node.parent.parent.is_null():
            return

        self._fix_insert(node)

    def delete(self: T, key: Any) -> None:
        self._delete_node_helper(self.root, key)

    def print_tree(self: T) -> str:
        return self.__print_helper(self.root, "", 'root')

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

    # Protected Methods

    # Balance the tree after insertion
    def _fix_insert(self: T, node: NodeBase) -> None:
        while node.parent.is_red():
            np = node.parent
            ngp = node.parent.parent
            if np == ngp.right:
                u = ngp.left
                if u.is_red():
                    u.color = "black"
                    np.color = "black"
                    ngp.color = "red"
                    node = ngp
                else:
                    if node == np.left:
                        node = np
                        self._right_rotate(node)
                    np_new = node.parent
                    np = np_new
                    np.color = "black"
                    ngp = np.parent
                    ngp.color = "red"
                    self._left_rotate(ngp)
            else:
                u = ngp.right

                if u.is_red():
                    u.color = "black"
                    np.color = "black"
                    ngp.color = "red"
                    node = ngp
                else:
                    if node == np.right:
                        node = np
                        self._left_rotate(node)
                    np_new = node.parent
                    np = np_new
                    np.color = "black"
                    ngp = np.parent
                    ngp.color = "red"
                    self._right_rotate(ngp)
            if node == self.root:
                break
        self.root.color = "black"

    # Printing the tree
    def __print_helper(self: T, node: NodeBase, indent: str, last: str) -> str:
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

    # Node deletion
    def _delete_node_helper(self: T, node: NodeBase, key: Any) -> None:
        z = self.search(key)
        if z.is_null():
            # Key not in tree.
            return

        y = z
        y_original_color = y.color
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
        if y_original_color == "black":
            self._delete_fix(x)

        self.size -= 1

    # Balancing the tree after deletion
    def _delete_fix(self: T, x: NodeBase) -> None:
        while x != self.root and x.is_black():
            np = x.parent
            assert isinstance(np, Node)
            if x == np.left:
                s = np.right
                if s.is_red():
                    s.color = "black"
                    np.color = "red"
                    self._left_rotate(np)
                    np_new = x.parent
                    assert isinstance(np_new, Node)
                    np = np_new
                    s = np.right

                if s.left.is_black() and s.right.is_black():
                    s.color = "red"
                    x = np
                else:
                    if s.right.is_black():
                        s.left.color = "black"
                        s.color = "red"
                        self._right_rotate(s)
                        np_new = x.parent
                        assert isinstance(np_new, Node)
                        np = np_new
                        s = np.right

                    s.color = np.color
                    np.color = "black"
                    s.right.color = "black"
                    self._left_rotate(np)
                    x = self.root
            else:
                s = np.left
                if s.is_red():
                    s.color = "black"
                    np.color = "red"
                    self._right_rotate(np)
                    np_new = x.parent
                    assert isinstance(np_new, Node)
                    np = np_new
                    s = np.left

                if s.left.is_black() and s.right.is_black():
                    s.color = "red"
                    x = np
                else:
                    if s.left.is_black():
                        s.right.color = "black"
                        s.color = "red"
                        self._left_rotate(s)
                        np_new = x.parent
                        np = np_new
                        s = np.left

                    s.color = np.color
                    np.color = "black"
                    s.left.color = "black"
                    self._right_rotate(np)
                    x = self.root
        x.color = "black"

    def __rb_transplant(self: T, u: NodeBase, v: NodeBase) -> None:
        if u.parent.is_null():
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _left_rotate(self: T, x: NodeBase) -> None:
        y = x.right
        x.right = y.left
        y.left.parent = x
        y.parent = x.parent
        if x.parent.is_null():
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self: T, x: NodeBase) -> None:
        y = x.left
        x.left = y.right
        y.right.parent = x

        y.parent = x.parent
        if x.parent.is_null():
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # Search the tree
    def _search_tree_helper(self: T, node: NodeBase, key: Any) -> NodeBase:
        if node.is_null() or key == node.key:
            return node

        if key < node.key:
            return self._search_tree_helper(node.left, key)
        return self._search_tree_helper(node.right, key)

    def _pre_order_helper(self: T, node: NodeBase,
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
            left = self._pre_order_helper(node.left, include_nulls)
            right = self._pre_order_helper(node.right, include_nulls)
        if include_nulls:
            basenode = [node]
        basenode.extend(left)
        basenode.extend(right)
        return basenode

    def _in_order_helper(self: T, node: NodeBase) -> str:
        """
        Create an array of child elements following
        a inorder traversal of the tree.
        """
        result = ""
        if not node.is_null():
            self._in_order_helper(node.left)
            result += str(node.key) + " "
            self._in_order_helper(node.right)
        return result

    def _post_order_helper(self: T, node: NodeBase) -> str:
        """
        Create an array of child elements following
        a postorder traversal of the tree.
        """
        result = ""
        if not node.is_null():
            self._post_order_helper(node.left)
            self._post_order_helper(node.right)
            result += str(node.key) + " "
        return result
