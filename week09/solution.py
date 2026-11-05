"""Solution, Week 9 MinHeap271 (Part A), posted after the deadline. Part B has no code; a Patient
with a (severity, arrival) key tuple is one acceptable design."""

class MinHeap271:
    """A priority queue that always returns its smallest value, stored as a
    complete binary tree in a Python list.

    storage -- the tree, level by level, left to right; the root is storage[0]
    """

    def __init__(self):
        # A new heap holds nothing: an empty list is an empty tree.
        self.storage: list = []

    # ---- Given: index arithmetic and swapping

    def _left_child(self, parent: int) -> int:
        # Each level doubles in size, so the children of position p sit at 2p+1 and 2p+2.
        return 2 * parent + 1

    def _right_child(self, parent: int) -> int:
        # The right child is always right next to the left child.
        return 2 * parent + 2

    def _parent(self, child: int) -> int:
        # Inverse of the two formulas above; // drops the remainder, so both
        # children of a node map back to the same parent.
        return (child - 1) // 2

    def _swap(self, i: int, j: int) -> None:
        # Save one value first; otherwise the first assignment would
        # overwrite it and we would lose it.
        temp = self.storage[i]
        # Copy the value at j into position i.
        self.storage[i] = self.storage[j]
        # Put the saved value into position j.
        self.storage[j] = temp

    def _is_leaf(self, position: int) -> bool:
        """Return True if position has no children in storage. A position has
        a child exactly when its left child is inside the list."""
        # The left child is the first child to appear in the list, so if even
        # that one is past the end, the node has no children at all.
        leaf = self._left_child(position) >= len(self.storage)
        return leaf

    # ---- TODO: restoring the heap property

    def _bubble_up(self) -> None:
        """Move the last value in storage up until its parent is not greater
        than it, or it reaches the root."""
        # The value just added is the last one in the list.
        position = len(self.storage) - 1
        # Keep climbing while we are not at the root (position 0) and the
        # value is smaller than its parent: that pair breaks the heap property.
        while position > 0 and self.storage[position] < self.storage[self._parent(position)]:
            # Swap with the parent, moving the value one level up.
            self._swap(position, self._parent(position))
            # Follow the value to its new position and check again.
            position = self._parent(position)

    def _sink_down(self) -> None:
        """Move the value at the root down until neither child is smaller
        than it, or it reaches a leaf."""
        # The value just moved to the top sits at position 0.
        position = 0
        # A leaf has no children, so there is nowhere further down to go.
        while not self._is_leaf(position):
            # Not a leaf, so the left child exists; assume it is the smaller child.
            small = self._left_child(position)
            # The right child may not exist (the last parent can have only one
            # child), so check that it is inside the list before looking at it.
            r = self._right_child(position)
            if r < len(self.storage) and self.storage[r] < self.storage[small]:
                # The right child exists and is smaller: it is the one to compare with.
                small = r
            if self.storage[position] > self.storage[small]:
                # Greater than its smaller child: swap, moving the value one level down.
                self._swap(position, small)
                # Follow the value to its new position and check again.
                position = small
            else:
                # Neither child is smaller, so the heap property holds: stop.
                break

    # ---- Given: the priority queue interface

    def size(self) -> int:
        """Return the number of values in the heap."""
        # The list holds exactly the values in the heap, nothing else.
        count = len(self.storage)
        return count

    def peek(self):
        """Return the smallest value without removing it; None if empty."""
        # Pessimistic default: an empty heap has no smallest value.
        smallest = None
        if len(self.storage) > 0:
            # The heap property puts the smallest value at the root.
            smallest = self.storage[0]
        return smallest

    def add(self, value) -> None:
        """Place value in the heap, keeping the minimum heap property."""
        # Put the new value in the next free spot at the bottom of the tree.
        self.storage.append(value)
        # It may be smaller than its parent, so let it float up if needed.
        self._bubble_up()

    def get(self):
        """Remove and return the smallest value; None if empty."""
        # Pessimistic default: an empty heap gives back None.
        smallest = None
        if len(self.storage) > 0:
            # The answer is the root.
            smallest = self.storage[0]
            # Pop the last leaf so the list has no gap.
            last = self.storage.pop()          # remove the last leaf
            # If that leaf was the root itself, the heap is now empty and
            # there is nothing to move; otherwise it takes the vacant root.
            if len(self.storage) > 0:          # something is left: move it to the root
                self.storage[0] = last
                # A leaf value is probably too big for the top: let it sink.
                self._sink_down()
        return smallest

    def __len__(self) -> int:
        # Lets len(heap) work: same as heap.size().
        return self.size()

    def __str__(self) -> str:
        # Shows the list, which is the whole tree level by level.
        return f"MinHeap271{self.storage}"
# Given -- tests. Run this cell after every change.
