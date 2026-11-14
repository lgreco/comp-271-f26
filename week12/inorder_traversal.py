"""In-order traversal of a binary search tree, two ways (class of 11/13).

This is the clean, runnable version of the code on the slides. It gives you
the ANSWER for each tree: the order in which the nodes are processed. It does
not show you HOW it got there, and that's on purpose. The how is your
assignment: trace both versions by hand, on paper.

    in_order_recursive  if the node is not empty: go left, process the node,
                        go right. The computer's call stack remembers where
                        to come back to.
    in_order_iterative  the same walk, but WE keep the stack: a plain list of
                        nodes we've passed on the way down and still owe a
                        visit.

"Processing" a node means appending its value to a list. On the slides it
meant printing; appending lets us compare the two versions' answers.
"""


class Node:
    """A node of a binary search tree of integers.

    The fields are public on purpose, as in week 11's bst.py, so the
    traversal code reads like the pseudocode on the slides.
    """

    def __init__(self, value: int):
        self.value = value  # the number stored in this node
        self.left = None  # root of the left subtree (smaller values)
        self.right = None  # root of the right subtree (larger values)


def insert(current: Node, value: int) -> Node:
    """Insert value below current and return the root of that subtree.

    The same recursive insert as week 11: smaller goes left, larger goes
    right, and a duplicate is ignored.
    """
    if current is None:
        current = Node(value)  # empty spot found: the new node lives here
    elif value < current.value:
        current.left = insert(current.left, value)
    elif value > current.value:
        current.right = insert(current.right, value)
    return current


def build_tree(values: list[int]) -> Node:
    """Insert values into an empty tree, in the given order, and return its
    root. The order matters: the same numbers in a different order give a
    different tree."""
    root = None
    for value in values:
        root = insert(root, value)
    return root


def in_order_recursive(node: Node, visited: list[int]) -> None:
    """Append the values of the subtree at node to visited, in order.

    Three lines of logic, and the tree's recursive shape does the rest:
    every subtree is itself a tree, so "go left" is just the same function
    called on a smaller tree. An empty subtree (None) does nothing, and that
    is the base case that ends the recursion.
    """
    if node is not None:
        in_order_recursive(node.left, visited)  # everything smaller first
        visited.append(node.value)  # then this node
        in_order_recursive(node.right, visited)  # then everything larger


def in_order_iterative(root: Node) -> list[int]:
    """Return the values of the tree at root, in order, without recursion.

    The stack holds the nodes we've walked past on the way down the left
    side. We passed them because their smaller values come first, but we
    still owe each of them a visit. The node on top of the stack is always
    the next one to visit.
    """
    visited = []
    stack = []  # nodes we passed on the way down; top is the end of the list
    current = root

    # Keep going while there is somewhere left to go down (current) or a
    # node we still owe a visit (stack).
    while current is not None or len(stack) > 0:
        # Go left as far as possible, pushing every node we pass.
        while current is not None:
            stack.append(current)
            current = current.left

        # current is None: there is nothing further left. The top of the
        # stack is the smallest value not yet visited, so visit it.
        current = stack.pop()
        visited.append(current.value)

        # Its right subtree holds the values just larger than it. Go
        # there next. If it's empty, the next pass of the loop pops the
        # following node instead.
        current = current.right

    return visited


if __name__ == "__main__":
    # The three trees from the README, built by inserting these numbers in
    # this order into an empty tree.
    trees = {
        "Tree A (class, 11/13)": [50, 40, 60, 45, 55],
        "Tree B": [40, 30, 20, 10],
        "Tree C": [10, 20, 30, 40],
    }

    for name, values in trees.items():
        root = build_tree(values)
        recursive_answer = []
        in_order_recursive(root, recursive_answer)
        iterative_answer = in_order_iterative(root)
        print(f"{name}, inserted as {values}")
        print(f"    recursive: {recursive_answer}")
        print(f"    iterative: {iterative_answer}")
