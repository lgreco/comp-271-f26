"""
Array271 -- a fixed-capacity string array, built on top of a Python list.
LONDON'S VERSION
This is the Week 2 `Array271` (see `week02/array_271.py`) carried forward
and extended with what we covered in class this week: private attributes
with accessor ("getter") methods instead of reaching into the object
directly, a `__str__` so printing an object shows something useful, a
`resize` that actually works, and a first `remove`.

Encapsulation, in short: every attribute is named with a leading
underscore (`_capacity`, not `capacity`) as a signal of "please don't
reach in here directly" -- Python doesn't enforce this, unlike Java or
C++, so it's a convention we agree to respect, not a wall. Reading or
changing an attribute from outside the class should always go through a
method (a getter, or a method like `add` that changes state on your
behalf).

This file is intentionally incomplete in one place: `remove` works, but
only partially -- see its docstring, and this week's `README.md`, for the
two modifications that are your assignment.
"""

from math import ceil


class Array271:
    """A fixed-capacity array of strings, backed by a Python list.

    Private attributes (leading underscore -- see module docstring):

        _capacity (int):
            How many string slots this array currently has room for,
            whether they're all in use or not.

        _resize_factor (float):
            How aggressively the array grows when it runs out of room.
            Expressed as a fraction of the current capacity to add, e.g.
            0.25 means "grow capacity by 25% when you resize."

        _occupancy (int):
            How many slots are actually holding a string right now.
            Always satisfies 0 <= occupancy <= capacity.

        _items (list):
            The underlying Python list that actually stores the strings.
            Pre-sized to `_capacity` and padded with None past the last
            occupied slot -- treat index `_occupancy` and beyond as empty,
            even though Python itself doesn't enforce that for us.
    """

    def __init__(self, capacity: int = 2, resize_factor: float = 0.25):
<<<<<<< HEAD
        """Construct an empty Array271.

        Parameters:
            capacity (int): initial number of slots to reserve. Defaults
                to 2 -- small on purpose, so a resize happens almost
                immediately in testing instead of being a rare edge case.
            resize_factor (float): how much to grow capacity by (as a
                fraction of current capacity) when the array fills up.
                Defaults to 0.25 (grow by 25%).
        """
        self._capacity: int = capacity
        self._resize_factor: float = resize_factor
        self._occupancy: int = 0
        self._items: list = [None] * capacity

    def __str__(self) -> str:
        """Return a human-readable summary: capacity, occupancy, and the
        occupied slots only (not the trailing Nones)."""
        occupied = self._items[: self._occupancy]
        return (
            f"Array271(capacity={self._capacity}, "
            f"occupancy={self._occupancy}, items={occupied})"
        )

    # ------------------------------------------------------------------
    # Accessors -- the only sanctioned way to read a private attribute
    # from outside the class.
    # ------------------------------------------------------------------

    def get_capacity(self) -> int:
        return self._capacity

    def get_resize_factor(self) -> float:
        return self._resize_factor

    def get_occupancy(self) -> int:
        return self._occupancy

    def get_items(self) -> list:
        return self._items

    def get_item(self, i: int):
        """Return the string at index i, or None if i is out of range.
=======
        self.__capacity: int = capacity
        self.__resize_factor: float = resize_factor
        self.__occupancy: int = 0
        self.__items: list = [None] * capacity

    def __str__(self):
        return f"Array271(capacity={self.__capacity}, resize_factor={self.__resize_factor}, occupancy={self.__occupancy}, items={self.__items})"

    def get_capacity(self):
        return self.__capacity
    def get_resize_factor(self):
        return self.__resize_factor
    def get_occupancy(self):
        return self.__occupancy
    def get_items(self):
        return self.__items

    def get_item(self, i):
        item = None
        if i >=0 and i < self.__occupancy:
            item = self.__items[i]
        return item
>>>>>>> 3baf6b2 (sy)

        "Out of range" means outside the *occupied* portion of the array
        (0 <= i < occupancy) -- an index that's within capacity but past
        occupancy would just return None anyway (that slot is empty), and
        a negative or too-large index would otherwise raise an
        IndexError. Failing gracefully (returning None) instead of
        crashing is the point: a bad index is the caller's mistake, not a
        reason to bring the whole program down.
        """
        item = None
        if 0 <= i < self._occupancy:
            item = self._items[i]
        return item

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def add(self, value: str):
<<<<<<< HEAD
        """Add a string to the array, growing it first if necessary.

        1. If occupancy has reached capacity, there's no free slot left,
           so grow the underlying storage first by calling `_resize()`.
        2. Place `value` at index `occupancy` -- the next free slot,
           since slots 0..occupancy-1 are already in use.
        3. Increment occupancy by 1.
        """
        if self._occupancy == self._capacity:
            self._resize()

        self._items[self._occupancy] = value
        self._occupancy += 1

    def remove(self, i: int) -> bool:
        """Remove the string at index i. Returns True on success, False
        if i isn't a valid occupied index.

        Current behavior (as built in class): bounds-check, then set that
        slot back to None. That's all -- the slot goes empty, but nothing
        moves.

        This leaves two problems, and fixing them is this week's
        assignment (see README.md):

        1. This returns a success flag, not the string that was removed.
           A caller who wants to know *what* they removed can't find out.
        2. The array now has a "hole": slots after index i still hold
           their strings, but the array is only supposed to treat
           0..occupancy-1 as occupied. The next `add` will overwrite
           `items[occupancy]`, not fill the hole at i -- silently leaving
           the removed slot's neighbors in the wrong place relative to
           where new items land. The fix is to shift every element after
           i down by one and decrement occupancy, so occupied slots stay
           contiguous starting at 0. And once removals leave the array
           mostly empty, it should be able to shrink, not just grow.
        """
        success = 0 <= i < self._occupancy
        if success:
            self._items[i] = None
        return success

    # ------------------------------------------------------------------
    # Internal helpers -- the leading underscore signals "don't call this
    # from outside the class"; `add` and `remove` are the public
    # interface, `_resize` is an implementation detail they lean on.
    # ------------------------------------------------------------------

    def _resize(self):
        """Grow capacity by `_resize_factor`, copying existing items over.

        `ceil` (rather than plain truncation) guarantees at least one new
        slot even when capacity * resize_factor rounds down to a
        fraction, e.g. 2 * 0.25 = 0.5 -- truncating that to 0 would grow
        the array by nothing and defeat the whole point.
        """
        growth = ceil(self._capacity * (1 + self._resize_factor))
        temp = [None] * growth
        for i in range(self._capacity):
            temp[i] = self._items[i]
        self._items = temp
        self._capacity = growth
=======
        if self.__occupancy == self.__capacity:
            self.__resize()
        self.__items[self.__occupancy] = value
        self.__occupancy += 1

    def __resize(self):
        growth = ceil(self.__capacity*(1+self.__resize_factor))
        temp = [None] * growth
        for i in range(self.__capacity):
            temp[i] = self.__items[i]
        self.__items = temp
        self.__capacity = growth

"""
    def remove(self, i):
        success = False
        if i >= 0 and i< self.__occupancy:
            success = True
            self.__items[i] = None
        return success
"""

    def remove(self, i):
        success = i >= 0 and i < self.__occupancy
        if success:
            self.__items[i] = None
        return success
>>>>>>> 3baf6b2 (sy)
