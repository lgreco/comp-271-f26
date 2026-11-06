"""The Python binary search tree from class, with search added.

This is the REFERENCE for the Java you write this week. You do not turn it in.
Read the two search methods and compare them with insert: all three walk the
same path from the root, going left for smaller and right for larger.
"""


class Node:
    """A node of a binary search tree of strings.

    The fields are public on purpose (no get/set methods) to keep the code
    simple. In Java the same fields are private, with accessors.
    """

    def __init__(self, value: str):
        self.value = value  # the string stored in this node
        self.left = None  # root of the left subtree (smaller values)
        self.right = None  # root of the right subtree (larger values)

    def __str__(self) -> str:
        return str(self.value)

    def __lt__(self, other) -> bool:
        """Order nodes by their values. Python derives > from <, so > works
        too. There is no __eq__, so == compares identity, not values; that is
        why the code below tests 'neither smaller nor larger' for a match."""
        return self.value < other.value


class BinarySearchTree:
    """A binary search tree of strings with no duplicates."""

    def __init__(self):
        self.root = None  # top node of the tree; None while the tree is empty
        self.size = 0  # number of nodes in the tree (distinct values)

    def insert(self, value: str) -> None:
        """Wrap value in a Node and add it, unless it is already present."""
        new_node = Node(value)
        # Reassigning the root is what makes the first insert work.
        self.root = self.insert_rec(self.root, new_node)

    def insert_rec(self, current_node, new_node):
        """Insert new_node below current_node; return the subtree's root."""
        if current_node is None:
            self.size += 1  # empty spot found: the new node lives here
            current_node = new_node
        elif new_node < current_node:
            current_node.left = self.insert_rec(current_node.left, new_node)
        elif new_node > current_node:
            current_node.right = self.insert_rec(current_node.right, new_node)
        # Neither smaller nor larger: a duplicate, so do nothing.
        return current_node

    def search(self, value: str) -> bool:
        """Return True if value is in the tree (recursive version, 11/2)."""
        found = self.search_rec(self.root, Node(value))
        return found

    def search_rec(self, current_node, target) -> bool:
        """Return True if target's value is in the subtree at current_node."""
        found = False  # pessimistic: an empty subtree has no target
        if current_node is not None:
            if target < current_node:
                found = self.search_rec(current_node.left, target)
            elif target > current_node:
                found = self.search_rec(current_node.right, target)
            else:
                found = True  # neither smaller nor larger: a match
        return found

    def search_iterative(self, value: str) -> bool:
        """Return True if value is in the tree (iterative version, 11/4)."""
        target = Node(value)
        current = self.root  # start at the entry point
        found = False
        while current is not None and not found:
            if target < current:
                current = current.left
            elif target > current:
                current = current.right
            else:
                found = True
        return found


if __name__ == "__main__":
    tree = BinarySearchTree()
    for word in "now is the winter of our discontent".split():
        tree.insert(word)
    print(tree.search("winter"), tree.search_iterative("winter"))  # True True
    print(tree.search("summer"), tree.search_iterative("summer"))  # False False
