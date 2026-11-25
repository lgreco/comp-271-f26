from __future__ import annotations  # for cool type hinting


# ---------------------------------------------------------------------------
# STUDENT REVIEW NOTES
# ---------------------------------------------------------------------------
# A Huffman tree uses ONE node class for two different roles:
#
#   LEAF node      symbol = a character (e.g. 'e'), frequency = how many
#                  times that character appears in the message, no children.
#
#   INTERNAL node  symbol = None, frequency = sum of the frequencies of its
#                  two children (and therefore of every leaf below it),
#                  exactly two children.
#
# Invariant worth checking on paper: the frequency stored at the ROOT equals
# the length of the original message, because every character is counted in
# exactly one leaf.
#
# The fields are private (double underscore), so the rest of the program
# talks to a node only through the accessor ("get_"/"has_") and mutator
# ("set_") methods below. That is encapsulation: Huffman never reaches into
# a node's fields directly.
# ---------------------------------------------------------------------------


class Node:
    """A simple binary tree node for a basic Huffman encoder."""

    def __init__(self, symbol: str | None, frequency: int):
        """Object constructor.

        Inputs
        ------
        (Note: the parameters appear below in the reverse order of the
        signature. Call it as Node(symbol, frequency).)
        frequency : int
          The frequency represented by this node. If the node has also a symbol,
          this is the frequency of the symbol. If no symbol is present, this is
          the sum of frequencies of the node's subtrees.
        symbol : char
          The symbol whose frequency we capture. If symbol is None, the node
          captures frequencies for subtrees under the node.

        Returns
        -------
        Instance of Node object with fields:
          frequency : as described above
          symbol : as described above
          left : pointer to left node child (default none)
          right : pointer to right node child (default none)
        """
        self.__frequency: int = frequency
        self.__symbol: str | None = symbol
        self.__left: None | Node = None
        self.__right: None | Node = None

    def __lt__(self, other: Node):
        """Redefine < for node to be based on frequency value"""
        # This "dunder" (double-underscore) method is called by Python
        # whenever it evaluates  node_a < node_b. Defining it is what lets
        # Huffman.__smallest_node compare nodes directly. It also makes
        # Node objects usable with sorted(), min(), and the heapq module,
        # which all rely on "<" alone.
        #
        # Why other.get_frequency() and not other.__frequency? Both work
        # inside the class, but going through the accessor is consistent
        # with how every other part of the program reads a node.
        return self.__frequency < other.get_frequency()

    def set_left(self, left: Node | None):
        """Setter for left child."""
        self.__left = left

    def set_right(self, right: Node | None):
        """Setter for right child."""
        self.__right = right

    def has_left(self):
        """Predicate accessor for left child"""
        return self.__left is not None

    def has_right(self):
        """Predicate accessor for right child"""
        return self.__right is not None

    def get_left(self):
        """Accessor for left child"""
        return self.__left

    def get_right(self):
        """Accessor for right child."""
        return self.__right

    def get_symbol(self) -> str:
        """Accessor for the symbol in a leaf node"""
        # Careful: for an internal node this returns None, even though the
        # type hint says str. Only call it on nodes where is_leaf() is True.
        return self.__symbol

    def get_frequency(self):
        """Accessor for frequency."""
        return self.__frequency

    def is_leaf(self) -> bool:
        """Determines if node is leaf node, indicated by the
        absence of both child pointers."""
        # In a Huffman tree "is a leaf" and "has a symbol" mean the same
        # thing, so we could have tested  self.__symbol is not None  instead.
        # Testing the children is the more general definition of a leaf and
        # works for any binary tree.
        return self.__left is None and self.__right is None

    def __str__(self):
        """String representation of object."""
        # Called by print(node) and str(node). Handy for debugging: print
        # the forest to watch nodes being merged, e.g.
        #     print([str(n) for n in forest])
        # Internal nodes will show up as [ None: 42 ].
        return f"[ {self.__symbol}: {self.__frequency} ]"
