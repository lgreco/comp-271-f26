"""Reading the codes off a Huffman tree, iteratively (class of 11/20).

This is the clean, runnable version of the traversal we wrote together. It
uses the "hello world" tree we built by hand on 11/18, typed in node by node
below, so that everyone traces the same tree. (Building the tree from the
frequencies is the next homework, not this one.)

The traversal keeps a "notepad": a plain list of [node, path so far] pairs.
While the notepad is not empty, pull an item out of it. If the node has
children, write them on the notepad with the path extended by "0" (left) or
"1" (right). If the node is a leaf, its path is its code.

Running this file prints the finished dictionary, nothing more. It gives you
the ANSWER. How the notepad fills and empties on the way there is your work:
trace it by hand, on paper.
"""


class Node:
    """A node of a Huffman tree.

    A leaf holds a symbol and how often it occurs. An internal node holds no
    symbol (None), only the combined frequency of the leaves below it.
    The fields are public on purpose, as in weeks 11 and 12, so the code
    reads like the pseudocode from class.
    """

    def __init__(self, symbol, frequency: int, left=None, right=None):
        self.symbol = symbol  # a one-character string, or None if internal
        self.frequency = frequency  # how many times the symbol(s) below occur
        self.left = left  # left child: its path gets a "0"
        self.right = right  # right child: its path gets a "1"

    def is_leaf(self) -> bool:
        """A node with no children is a leaf, and only leaves carry symbols."""
        return self.left is None and self.right is None

    def get_symbol(self):
        """The symbol stored in this node (None for an internal node)."""
        return self.symbol


def hello_world_tree() -> Node:
    """Return the root of the Huffman tree for "hello world" from 11/18.

    Frequencies: l 3, o 2, and h, e, space, w, r, d once each: 11 in all.

                              (11)
                       0 /           \\ 1
                       (7)             (4)
                   0 /     \\ 1     0 /     \\ 1
                   (4)      l:3     (2)       (2)
               0 /    \\ 1       0 /  \\ 1   0 /  \\ 1
               (2)     o:2      ' ':1  w:1  r:1   d:1
           0 /    \\ 1
           h:1    e:1
    """
    h_e = Node(None, 2, Node("h", 1), Node("e", 1))
    h_e_o = Node(None, 4, h_e, Node("o", 2))
    left_half = Node(None, 7, h_e_o, Node("l", 3))
    space_w = Node(None, 2, Node(" ", 1), Node("w", 1))
    r_d = Node(None, 2, Node("r", 1), Node("d", 1))
    right_half = Node(None, 4, space_w, r_d)
    return Node(None, 11, left_half, right_half)


def get_codes(root: Node) -> dict:
    """Return a dictionary mapping each symbol in the tree to its code.

    The code of a symbol is the path from the root to its leaf: "0" for
    every step left, "1" for every step right.
    """
    codes = dict()
    notepad = [[root, ""]]  # one item to start with: the root, no path yet

    # Keep going until there is nothing left on the notepad.
    while len(notepad) > 0:
        # Pull an item out and unpack it. pop() takes the LAST item, so the
        # notepad behaves as a stack. (Part 1, step 4: what if pop(0)?)
        node, path = notepad.pop()

        # Write each child on the notepad, one step further along the path.
        if node.left is not None:
            notepad.append([node.left, path + "0"])
        if node.right is not None:
            notepad.append([node.right, path + "1"])

        # A leaf ends a path: the path walked to reach it is its code.
        if node.is_leaf():
            codes[node.get_symbol()] = path

    return codes


def encode(message: str, codes: dict) -> str:
    """Replace every character of message with its code."""
    bits = ""
    for char in message:
        bits += codes[char]
    return bits


if __name__ == "__main__":
    message = "hello world"
    codes = get_codes(hello_world_tree())

    # The dictionary, in the order its entries were added. The order is a
    # useful check on your trace: it is the order the leaves came off the
    # notepad.
    print(f"codes: {codes}")

    bits = encode(message, codes)
    print(f"{message!r} in ASCII: {8 * len(message)} bits")
    print(f"{message!r} in Huffman: {len(bits)} bits: {bits}")
