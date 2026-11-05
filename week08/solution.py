"""
Week 8 -- solution, posted after the deadline.

Part 1: merge_sort_iterative (bottom-up).
Part 2: ArrayQueue271 (circular) and ArrayStack271 (plain), both on a
fixed-capacity array.
"""

from __future__ import annotations


def merge(a: list[int], b: list[int]) -> list[int]:
    """Merge two already-sorted lists into one new sorted list."""
    c: list[int] = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    while i < len(a):
        c.append(a[i])
        i += 1
    while j < len(b):
        c.append(b[j])
        j += 1
    return c


def merge_sort(arr: list[int]) -> list[int]:
    """Recursive merge sort, as written in class. Returns a new list."""
    result = arr
    if len(arr) > 1:
        mid = len(arr) // 2
        sorted_left = merge_sort(arr[:mid])
        sorted_right = merge_sort(arr[mid:])
        result = merge(sorted_left, sorted_right)
    return result


def merge_sort_iterative(arr: list[int]) -> list[int]:
    """Bottom-up merge sort: no recursion. Returns a new list."""
    result = list(arr)
    width = 1
    while width < len(result):
        merged: list[int] = []
        for start in range(0, len(result), 2 * width):
            left = result[start:start + width]
            right = result[start + width:start + 2 * width]
            merged.extend(merge(left, right))
        result = merged
        width *= 2
    return result


class ArrayQueue271:
    """FIFO queue on a fixed-capacity array that wraps around."""

    def __init__(self, capacity: int = 4):
        self.capacity: int = capacity
        self.storage: list = [None] * capacity
        self.front: int = 0   # index of the next item to remove
        self.back: int = 0    # index where the next item will be written
        self.used: int = 0

    def __len__(self) -> int:
        return self.used

    def is_empty(self) -> bool:
        return self.used == 0

    def is_full(self) -> bool:
        return self.used == self.capacity

    def add(self, item) -> bool:
        """Add item at the back. Return False (and change nothing) if full."""
        added = False
        if not self.is_full():
            self.storage[self.back] = item
            self.back = (self.back + 1) % self.capacity
            self.used += 1
            added = True
        return added

    def remove(self):
        """Remove and return the front item, or None if empty."""
        item = None
        if not self.is_empty():
            item = self.storage[self.front]
            self.storage[self.front] = None
            self.front = (self.front + 1) % self.capacity
            self.used -= 1
        return item

    def __str__(self) -> str:
        return f"{self.storage} front={self.front} back={self.back} used={self.used}"


class ArrayStack271:
    """LIFO stack on a fixed-capacity array, filled from the back toward index 0."""

    def __init__(self, capacity: int = 4):
        self.capacity: int = capacity
        self.storage: list = [None] * capacity
        self.top: int = capacity - 1   # index where the next item will be written
        self.used: int = 0

    def __len__(self) -> int:
        return self.used

    def is_empty(self) -> bool:
        return self.used == 0

    def is_full(self) -> bool:
        return self.used == self.capacity

    def add(self, item) -> bool:
        """Push item. Return False (and change nothing) if full."""
        added = False
        if not self.is_full():
            self.storage[self.top] = item
            self.top -= 1
            self.used += 1
            added = True
        return added

    def remove(self):
        """Pop and return the most recently added item, or None if empty."""
        item = None
        if not self.is_empty():
            self.top += 1
            item = self.storage[self.top]
            self.storage[self.top] = None
            self.used -= 1
        return item

    def __str__(self) -> str:
        return f"{self.storage} top={self.top} used={self.used}"
