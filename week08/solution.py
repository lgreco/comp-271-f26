"""
Week 8 -- solution, posted after the deadline.

Part 1: merge_sort_iterative (bottom-up).
Part 2: ArrayQueue271 (circular) and ArrayStack271 (plain), both on a
fixed-capacity array.
"""

from __future__ import annotations


def merge(a: list[int], b: list[int]) -> list[int]:
    """Merge two already-sorted lists into one new sorted list."""
    # The output list, built one element at a time. Neither input is changed.
    c: list[int] = []
    # i is our finger on a, j is our finger on b; both start at the front.
    # (i = j = 0 assigns the same value to both names.)
    i = j = 0
    # Phase 1: while BOTH lists still have unread elements, the smaller of the
    # two front elements must come next, because each list is already sorted.
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            # a's front is smaller: copy it out and advance a's finger.
            c.append(a[i])
            i += 1
        else:
            # b's front is smaller (or tied): copy it out and advance b's finger.
            # On a tie we take from b; either choice gives a correct sorted result.
            c.append(b[j])
            j += 1
    # Phase 2: at most one of the two loops below runs. Whichever list still
    # has elements left holds values that are all >= everything already in c,
    # and they are already in order, so we copy them over unchanged.
    while i < len(a):
        c.append(a[i])
        i += 1
    while j < len(b):
        c.append(b[j])
        j += 1
    # The single return: the merged, sorted list.
    return c


def merge_sort(arr: list[int]) -> list[int]:
    """Recursive merge sort, as written in class. Returns a new list."""
    # Base case, by pessimistic default: a list of 0 or 1 elements is already
    # sorted, so it is returned as is and nothing below overwrites it.
    result = arr
    if len(arr) > 1:
        # Split point: the middle index (// is integer division).
        mid = len(arr) // 2
        # Recursive case: sort each half independently. Slicing makes copies,
        # so the original list is untouched.
        sorted_left = merge_sort(arr[:mid])
        sorted_right = merge_sort(arr[mid:])
        # The "conquer" step: weave the two sorted halves into one sorted list.
        result = merge(sorted_left, sorted_right)
    return result


def merge_sort_iterative(arr: list[int]) -> list[int]:
    """Bottom-up merge sort: no recursion. Returns a new list."""
    # Work on a copy so the caller's list is not modified.
    result = list(arr)
    # width is the length of the already-sorted runs. Every single element is
    # a sorted run of length 1, which is where the recursion would bottom out.
    width = 1
    # Each pass merges neighboring runs into runs twice as long; once a run
    # is as long as the whole list, we are done.
    while width < len(result):
        # This pass's output, built from scratch.
        merged: list[int] = []
        # Jump from one pair of runs to the next: each pair covers 2 * width items.
        for start in range(0, len(result), 2 * width):
            # The first run of the pair, then the one right after it. Slices
            # stop quietly at the end of the list, so a leftover short run
            # (or a missing second run) needs no special handling.
            left = result[start:start + width]
            right = result[start + width:start + 2 * width]
            # merge() produces one sorted run; extend() appends all of it.
            merged.extend(merge(left, right))
        # The merged list becomes the input of the next pass.
        result = merged
        # Runs have doubled in length: 1, 2, 4, 8, ...
        width *= 2
    return result


class ArrayQueue271:
    """FIFO queue on a fixed-capacity array that wraps around."""

    def __init__(self, capacity: int = 4):
        # The array never grows; this is its fixed size.
        self.capacity: int = capacity
        # Pre-allocate every slot, empty (None) for now.
        self.storage: list = [None] * capacity
        self.front: int = 0   # index of the next item to remove
        self.back: int = 0    # index where the next item will be written
        # We track the count separately because front == back is ambiguous:
        # it happens both when the queue is empty and when it is full.
        self.used: int = 0

    def __len__(self) -> int:
        # Lets len(queue) work.
        return self.used

    def is_empty(self) -> bool:
        # Nothing stored.
        return self.used == 0

    def is_full(self) -> bool:
        # Every slot is occupied.
        return self.used == self.capacity

    def add(self, item) -> bool:
        """Add item at the back. Return False (and change nothing) if full."""
        # Pessimistic default: assume the add fails until it succeeds.
        added = False
        if not self.is_full():
            # Write the item into the next free slot.
            self.storage[self.back] = item
            # Advance back by one; % capacity wraps it from the last index
            # to index 0, which is what makes the array "circular".
            self.back = (self.back + 1) % self.capacity
            # One more item is stored.
            self.used += 1
            added = True
        return added

    def remove(self):
        """Remove and return the front item, or None if empty."""
        # Pessimistic default: an empty queue gives back None.
        item = None
        if not self.is_empty():
            # Take the oldest item, the one at the front.
            item = self.storage[self.front]
            # Clear the slot so a stale value is never mistaken for live data.
            self.storage[self.front] = None
            # Advance front by one, wrapping around the end of the array.
            self.front = (self.front + 1) % self.capacity
            # One fewer item is stored.
            self.used -= 1
        return item

    def __str__(self) -> str:
        # Shows the raw array plus the bookkeeping, handy for tracing wraparound.
        return f"{self.storage} front={self.front} back={self.back} used={self.used}"


class ArrayStack271:
    """LIFO stack on a fixed-capacity array, filled from the back toward index 0."""

    def __init__(self, capacity: int = 4):
        # The array never grows; this is its fixed size.
        self.capacity: int = capacity
        # Pre-allocate every slot, empty (None) for now.
        self.storage: list = [None] * capacity
        # top points at the next FREE slot, not at the newest item. It starts
        # at the last index and moves toward 0 as the stack fills.
        self.top: int = capacity - 1   # index where the next item will be written
        self.used: int = 0

    def __len__(self) -> int:
        # Lets len(stack) work.
        return self.used

    def is_empty(self) -> bool:
        # Nothing stored.
        return self.used == 0

    def is_full(self) -> bool:
        # Every slot is occupied.
        return self.used == self.capacity

    def add(self, item) -> bool:
        """Push item. Return False (and change nothing) if full."""
        # Pessimistic default: assume the push fails until it succeeds.
        added = False
        if not self.is_full():
            # Write the item into the free slot top points at.
            self.storage[self.top] = item
            # Move top one slot toward index 0. No wraparound is needed:
            # a stack only ever grows and shrinks at this one end.
            self.top -= 1
            self.used += 1
            added = True
        return added

    def remove(self):
        """Pop and return the most recently added item, or None if empty."""
        # Pessimistic default: an empty stack gives back None.
        item = None
        if not self.is_empty():
            # top points at a free slot, so the newest item is one slot
            # above it: step back first, then read.
            self.top += 1
            item = self.storage[self.top]
            # Clear the slot; it is the free slot top points at again.
            self.storage[self.top] = None
            self.used -= 1
        return item

    def __str__(self) -> str:
        # Shows the raw array plus top, handy for tracing pushes and pops.
        return f"{self.storage} top={self.top} used={self.used}"
