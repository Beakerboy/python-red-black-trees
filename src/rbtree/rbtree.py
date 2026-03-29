from typing import Any, Optional, TypeVar, Iterator
from enum import Enum
from rbtree.node import Node
from rbtree.node_base import NodeBase


class IteratorType(Enum):
    PRE = -1
    IN = 0
    POST = 1


T = TypeVar('T', bound='RedBlackTree')


class RedBlackTree():
    def __init__(self: T) -> None:
        self._root: NodeBase = NodeBase.NIL
        self.size = 0
        self._iterator_include_nulls = False
        self._traversal_type = IteratorType.PRE

    # Dunder Methods

    def __iter__(self: T) -> Iterator:
        nulls = self._iterator_include_nulls
        match self._traversal_type:
            case IteratorType.PRE:
                return iter(self.preorder(nulls))
            case IteratorType.IN:
                return iter(self.inorder(nulls))
            case IteratorType.POST:
                return iter(self.postorder(nulls))

    def __len__(self: T) -> int:
        return self.size

    def __str__(self: T) -> str:
        return self.__print_helper(self.root, "", 'root')

    # Getters and Setters and Properties
    @property
    def root(self: T) -> NodeBase:
        return self._root

    # Public Methods

    def include_nulls(self: T) -> None:
        """
        Configure the iterator to include nulls
        """
        self._iterator_include_nulls = True

    def exclude_nulls(self: T) -> None:
        """
        Configure the iterator to exclude nulls
        """
        self._iterator_include_nulls = False

    def use_preorder(self: T) -> None:
        self._traversal_type = IteratorType.PRE

    def use_postorder(self: T) -> None:
        self._traversal_type = IteratorType.POST

    def use_inorder(self: T) -> None:
        self._traversal_type = IteratorType.IN

    def preorder(self: T, include_nulls: bool = False) -> list:
        return self._pre_order_helper(self.root, include_nulls)

    def inorder(self: T, include_nulls: bool = False) -> list:
        return self._in_order_helper(self.root, include_nulls)

    def postorder(self: T, include_nulls: bool = False) -> list:
        return self._post_order_helper(self.root, include_nulls)

    def search(self: T, key: Any) -> NodeBase:
        """
        Find the node with the given key
        """
        node: NodeBase
        if isinstance(key, NodeBase):
            node = key
        else:
            node = Node(key)
        return self._search_tree_helper(self.root, node)

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
            return node
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

    def predecessor(self: T,  x: NodeBase) -> Optional[NodeBase]:
        if (not x.left.is_null()):
            return self.maximum(x.left)

        y = x.parent
        while not y.is_null() and x == y.left:
            x = y
            y = y.parent

        return y

    def insert(self: T, key: Any) -> None:
        # Allow the user to provide a custom node.
        node: NodeBase
        if isinstance(key, NodeBase):
            node = key
        else:
            node = Node(key)
        y: NodeBase = NodeBase.NIL
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
            self._root = node
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
        node: NodeBase
        if isinstance(key, NodeBase):
            node = key
        else:
            node = Node(key)
        self._delete_node_helper(self.root, node)

    def to_mindmap(self: T) -> str:
        null_depths = []
        output = "@startmindmap\n"
        for node in self.preorder(True):
            if not node.is_null():
                if node.right.is_null():
                    null_depths.append(node.depth() + 1)
                if node.left.is_null():
                    null_depths.append(node.depth() + 1)
            color = "white" if node.is_black() else "red"
            depth = null_depths.pop() if node.is_null() else node.depth()
            output += (
                "-" * (depth + 1) + "[#" + color +
                r"] <latex>\rotatebox{-90}{" + str(node) + "}</latex>\n"
            )
        return output + "@endmindmap"

    # Protected Methods

    # Balance the tree after insertion
    def _fix_insert(self: T, node: NodeBase) -> None:
        while node.parent.is_red():
            np = node.parent
            ngp = node.parent.parent
            if not ngp.right.is_null() and np == ngp.right:
                u = ngp.left
                if u.is_red():
                    u.color = "black"
                    np.color = "black"
                    ngp.color = "red"
                    node = ngp
                else:
                    if not np.left.is_null() and node == np.left:
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
                    if not np.right.is_null() and node == np.right:
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
            output += str(node) + "(" + s_color + ")\n"
            output += self.__print_helper(node.left, indent, 'not_last')
            output += self.__print_helper(node.right, indent, 'last')
        return output

    def _delete_node_helper(
            self: T, node: NodeBase, node_to_delete: NodeBase) -> None:
        """
        Remove the node from the tree.
        Reorganize the tree to maintain validity.
        """
        z = self.search(node_to_delete)
        if z.is_null():
            # Key not in tree.
            return

        y = z
        y_original_color = y.color
        np = z.parent
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
            if y.parent == z and not x.is_null():
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                if not y.right.is_null():
                    y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            if not y.left.is_null():
                y.left.parent = y
            y.color = z.color
        if y_original_color == "black":
            self._delete_fix(x, np)

        self.size -= 1

    # Balancing the tree after deletion
    def _delete_fix(self: T, x: NodeBase, np: NodeBase) -> None:
        while x != self.root and x.is_black():
            if x == np.left:
                s = np.right
                if s.is_red():
                    s.color = "black"
                    np.color = "red"
                    self._left_rotate(np)
                    np_new = x.parent
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
        if u.parent.is_null():  # We are removing the root node
            self._root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if not v.is_null():
            v.parent = u.parent
        u.parent = NodeBase.NIL

    def _left_rotate(self: T, x: NodeBase) -> None:
        y = x.right
        x.right = y.left
        if not y.left.is_null():
            y.left.parent = x
        y.parent = x.parent
        if x.parent.is_null():
            self._root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self: T, x: NodeBase) -> None:
        y = x.left
        x.left = y.right
        if not y.right.is_null():
            y.right.parent = x
        y.parent = x.parent
        if x.parent.is_null():
            self._root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # Search the tree
    def _search_tree_helper(
            self: T, node: NodeBase, node_to_find: NodeBase) -> NodeBase:

        if node.is_null() or node_to_find.is_null():
            return NodeBase.NIL
        if node == node_to_find:
            return node

        if node_to_find < node:
            return self._search_tree_helper(node.left, node_to_find)
        return self._search_tree_helper(node.right, node_to_find)

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
        elif include_nulls:
            basenode = [node]
        basenode.extend(left)
        basenode.extend(right)
        return basenode

    def _in_order_helper(self: T, node: NodeBase,
                         include_nulls: bool = False) -> list:
        """
        Create an array of child elements following a inorder traversal of the
        tree.
        """
        basenode = []
        if not node.is_null():
            basenode = self._in_order_helper(node.left, include_nulls)
            basenode.extend([node])
            basenode.extend(self._in_order_helper(node.right, include_nulls))
        elif include_nulls:
            basenode = [node]
        return basenode

    def _post_order_helper(self: T, node: NodeBase,
                           include_nulls: bool = False) -> list:
        """
        Create an array of child elements following a postorder traversal of
        the tree.
        """
        basenode = []
        if not node.is_null():
            basenode = self._post_order_helper(node.left, include_nulls)
            basenode.extend(self._post_order_helper(node.right, include_nulls))
            basenode.extend([node])
        elif include_nulls:
            basenode = [node]
        return basenode

    @staticmethod
    def validate_red_black_tree(
            node: NodeBase,
            min_val: Optional[NodeBase] = None,
            max_val: Optional[NodeBase] = None,) -> tuple[bool, int)]:
        """
        Validates all Red-Black Tree properties in one pass.
        Returns (is_valid, black_height) or (False, -1).
        """
        # 1. Leaf Property: NIL nodes are always valid and have black height 0
        if node.is_null():
            return True, 0

        # 2. BST Property: Key must be within valid range
        if min_val is not None:
            if max_val is not None:
                if not min_val < node < max_val:
                    return False, -1
            else:
                if not min_val < node:
                    return False, -1
        else:
            if not node < max_val:
                return False, -1

        # 3. Red Property: No red node can have a red child
        # Note: node._red is True if red, False if black
        if node._red:
            if node.left.is_red() or node.right.is_red():
                return False, -1

        # Recursive checks for children
        left_valid, left_bh = RedBlackTree.validate_red_black_tree(
            node.left, min_val, node
        )
        right_valid, right_bh = RedBlackTree.validate_red_black_tree(
            node.right, node, max_val
        )

        if not left_valid or not right_valid:
            return False, -1

        # 4. Black Height Property: Left and right subtrees must have same
        # black height
        if left_bh != right_bh:
            return False, -1

        # Calculate current node's black height contribution
        # If node is black, height increases by 1
        current_bh = left_bh + (0 if node._red else 1)
        return True, current_bh

    def is_valid(self: T) -> bool:
        if self._root.is_null():
            return True

        # 5. Root Property: Root must be black
        if self._root._red:
            return False

        valid, _ = RedBlackTree.validate_red_black_tree(self._root)
        return valid
