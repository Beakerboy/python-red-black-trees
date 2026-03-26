# Python red-black trees
![Build Status](https://github.com/Beakerboy/python-red-black-trees/actions/workflows/python-package.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/Beakerboy/python-red-black-trees/badge.svg?branch=main)](https://coveralls.io/github/Beakerboy/python-red-black-trees?branch=main)

A Python implementation of red-black trees. This implementation is unique in that instead of hiding the nodes within the implementation, the nodes are easily seen so that the user can inspect the color and relationships between bodes at any time. Highly specialized comparison functions can be specified to determine which bose is greater than or less than another

## What is this for?

This implementation was created for MS-CFB, a project where files must be saved in a Red Black Tree, and this tree stricture is to be saved to disk. Most Red Black Tree implementations would use a dictionary sort when comparing which string is larger or smaller than another, but this project requires using the file name length along with converting to uppercase unicode. To accomodate custom sorting, this library requires the user to define dunder methods do imporm the tree which of two nodes is larger or smaller.

## Documentation


### Standard red-black tree interface

#### Constructor

A new red-black tree can be constructed as follows:

```
bst = RedBlackTree()
```

#### Insert

Items can be inserted into a tree using the `insert` method:

```
bst.insert(5)  # inserts a node with value 5
```

#### Delete

Items can be removed from the tree using the `delete` method. This method will do nothing if
there is no item in the tree with the specific key.

```
bst.delete(5)  # removes a node with value 5
```

#### Minimum and maximum

The minimum and maximum value in the tree can be found with the corresponding methods. If the tree is empty, these methods will both return the special value `bst.TNULL`

```
bst.minimum()  # returns minimum value
bst.maximum()  # returns maximum value

bst.minimum() == bst.TNULL  # Check whether tree is empty
```

#### Tree size

Tree size can be accessed via the `size` member variable:

```
bst.size  # contains the tree's size
```

#### Search

To find a specific item in the tree, you can use the search method:

```
bst.search(6)  # returns the node containing 6. Will return bst.TNULL if item is not present.
```

#### Predecessor and successor

To get a node's predecessor or sucessor;

```
bst.predecessor(bst.search(6))  # Gets the predecessor a node containing 6
bst.successor(bst.search(6))  # Gets the successor a node containing 6

```

#### Printing methods

To know more about the contents of the tree, you can use various printing methods:

```
bst.print_tree()  # prints an ASCII representation of the whole tree
bst.preorder()      # prints a preorder traversal
bst.inorder()       # prints an inorder traveral
bst.postorder()     # prints a postorder traversal
```

### Dictionary interface

```
bst[80] = 4  # Store the value 4 with the key 80
bst[80]      # Retrieve the value associated with the key 80
```
