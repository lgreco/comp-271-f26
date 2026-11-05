"""Solution, Week 9 MinHeap271 (Part A), posted after the deadline. Part B has no code; a Patient
with a (severity, arrival) key tuple is one acceptable design."""

class MinHeap271:
    """A priority queue that always returns its smallest value, stored as a
    complete binary tree in a Python list.

    storage -- the tree, level by level, left to right; the root is storage[0]
    """

    def __init__(self):
        self.storage: list = []

    # ---- Given: index arithmetic and swapping

    def _left_child(self, parent: int) -> int:
        return 2 * parent + 1

    def _right_child(self, parent: int) -> int:
        return 2 * parent + 2

    def _parent(self, child: int) -> int:
        return (child - 1) // 2

    def _swap(self, i: int, j: int) -> None:
        temp = self.storage[i]
        self.storage[i] = self.storage[j]
        self.storage[j] = temp

    def _is_leaf(self, position: int) -> bool:
        """Return True if position has no children in storage. A position has
        a child exactly when its left child is inside the list."""
        leaf = self._left_child(position) >= len(self.storage)
        return leaf

    # ---- TODO: restoring the heap property

    def _bubble_up(self) -> None:
        """Move the last value in storage up until its parent is not greater
        than it, or it reaches the root."""
        position = len(self.storage) - 1
        while position > 0 and self.storage[position] < self.storage[self._parent(position)]:
            self._swap(position, self._parent(position))
            position = self._parent(position)

    def _sink_down(self) -> None:
        """Move the value at the root down until neither child is smaller
        than it, or it reaches a leaf."""
        position = 0
        while not self._is_leaf(position):
            small = self._left_child(position)
            r = self._right_child(position)
            if r < len(self.storage) and self.storage[r] < self.storage[small]:
                small = r
            if self.storage[position] > self.storage[small]:
                self._swap(position, small)
                position = small
            else:
                break

    # ---- Given: the priority queue interface

    def size(self) -> int:
        """Return the number of values in the heap."""
        count = len(self.storage)
        return count

    def peek(self):
        """Return the smallest value without removing it; None if empty."""
        smallest = None
        if len(self.storage) > 0:
            smallest = self.storage[0]
        return smallest

    def add(self, value) -> None:
        """Place value in the heap, keeping the minimum heap property."""
        self.storage.append(value)
        self._bubble_up()

    def get(self):
        """Remove and return the smallest value; None if empty."""
        smallest = None
        if len(self.storage) > 0:
            smallest = self.storage[0]
            last = self.storage.pop()          # remove the last leaf
            if len(self.storage) > 0:          # something is left: move it to the root
                self.storage[0] = last
                self._sink_down()
        return smallest

    def __len__(self) -> int:
        return self.size()

    def __str__(self) -> str:
        return f"MinHeap271{self.storage}"
# Given -- tests. Run this cell after every change.
