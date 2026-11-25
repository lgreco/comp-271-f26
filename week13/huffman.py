from __future__ import annotations  # for cool type hinting
from tree_node import *

# ---------------------------------------------------------------------------
# STUDENT REVIEW NOTES -- the big picture
# ---------------------------------------------------------------------------
# Huffman coding is a *lossless* compression technique. Instead of giving
# every symbol the same number of bits (ASCII uses 8 bits for every
# character), it gives SHORT codes to FREQUENT symbols and LONG codes to
# RARE symbols. In English text, ' ' and 'e' show up constantly, so they
# get codes that are 2-4 bits long; 'Q' or '~' are rare and may get codes
# that are 15+ bits long. On average we come out well ahead.
#
# The pipeline implemented in this class is:
#
#   message --> frequencies --> forest of leaf nodes --> Huffman tree
#           --> encoder (symbol -> bit string) --> encoded message
#
# and in reverse:
#
#   encoded message + Huffman tree --> walk the tree bit by bit --> message
#
# Key idea to remember: symbols live ONLY in the LEAVES of the tree. A
# symbol's code is the path from the root to its leaf (left = 0,
# right = 1). Because no leaf sits on the path to another leaf, no code
# can be the beginning (prefix) of another code. This "prefix-free"
# property is what lets us decode a stream of bits WITHOUT separators
# between codes.
#
# A note on the private names: every method and field whose name starts
# with two underscores (e.g. __forest, __huffman_tree) is "name-mangled"
# by Python, which is Python's way of saying "internal, do not touch from
# outside the class." The only public methods are encode() and decode()
# at the bottom of the file.
# ---------------------------------------------------------------------------


class Huffman:

    # Encoding constants
    # We use the *characters* "0" and "1" rather than real bits. This keeps
    # the code readable, but it means the "compressed" string actually takes
    # MORE memory than the original: each "0"/"1" is itself a full
    # character. A production compressor would pack every 8 of these into
    # one byte (e.g., with int(chunk, 2) and a bytearray). When we report
    # compression ratios in test_huffman.py we count len(encoded) as BITS,
    # which is what it would be after packing.
    __LEFT = "0"
    __RIGHT = "1"
    __PROGRESS_BAR_LENGTH = 20

    def __init__(self, verbose: bool = False) -> None:
        """Constructor"""
        # Note: the constructor does no real work; it only declares the
        # fields and sets them to None. The fields get filled in, in order,
        # as encode() triggers the chain of private methods below. Typing
        # each field as "X | None" documents that it is empty until then.
        #
        # Message to encode/compress
        self.__message: str | None = None
        # Frequencies of symbols in message to encode. The information is
        # captured as key-value pairs, where symbols are keys and frequencies
        # are values.
        self.__frequency: dict | None = None
        # Forest of symbol-frequency nodes. This is the data structure
        # that the Huffman algorithm operates on to create the
        # Huffman tree.
        self.__forest: list[Node] | None = None
        # When Huffman is done iterating over the forest of symbol-frequency
        # nodes, the remaining node in the forest is the root of the Huffman
        # tree representing the prefix-free codes.
        self.__huffman_root: Node | None = None
        # A key-values strucuture with the prefix-free codes for each symbol
        # in the message to encode.
        self.__encoder: dict | None = None
        # The root of the Huffman tree to use for decoding a compressed
        # message.
        self.__decoder: Node | None = None
        # The encoded message
        self.__encoded: str | None = None
        # Verbose mode for debugging
        self.__verbose: bool = verbose

    def __count_frequencies(self) -> None:
        """Generates frequencies of symbols in a message to be encoded.
        The method populated the object's frequency dictionary with
        symbols as keys and frequencies as values."""
        # Cost: one pass over the message, and each dictionary lookup/update
        # is O(1) on average, so this step is O(n) for a message of n
        # symbols. This is the ONLY step (besides the final encoding loop)
        # whose cost depends on the length of the message. Everything that
        # follows depends on k, the number of UNIQUE symbols, which is tiny
        # by comparison (around 100 for English text, even for a whole book).
        #
        # Python shortcut worth knowing: collections.Counter(message) does
        # exactly this in one line. Writing it out by hand shows how it works.
        self.__frequency = dict()
        for c in self.__message:
            # Have we seen this symbol before?
            if c in self.__frequency:
                # Yes, increment its frequency
                self.__frequency[c] += 1
            else:
                # No, initialize its frequency to 1
                self.__frequency[c] = 1
        if self.__verbose:
            print(
                f"There are {len(self.__frequency):,d} unique symbols in the message."
            )

    def __build_forest(self) -> None:
        """Converts a key-value list of symbol-frequencies into a list of
        binary tree nodes with symbol and frequencies as their data
        payload."""
        # Why a "forest"? Each node here is a tiny one-node tree (a leaf).
        # Huffman's algorithm repeatedly merges trees in this forest until
        # only one tree remains. Every node created here will end up as a
        # LEAF of the final Huffman tree -- these are the only nodes that
        # carry a symbol.
        #
        # First obtain frequencies
        self.__count_frequencies()
        # Initialize a list of Node objects
        self.__forest: list[Node] = []
        # For every symbol-frequency pair, create a new node and add it
        # to the list of nodes
        for symbol, frequency in self.__frequency.items():
            self.__forest.append(Node(symbol, frequency))
        if self.__verbose:
            print(f"Built a forest of {len(self.__forest):,d} nodes.")

    def __smallest_node(self) -> Node:
        """Finds and returns the node with the least frequency from
        a list of nodes"""
        # This is a plain linear search for the minimum, followed by a
        # removal. Both are O(k) for a forest of k nodes:
        #   - the loop looks at every node once, and
        #   - list.pop(i) has to shift every element after position i one
        #     slot to the left.
        #
        # The comparison below uses "<" between two Node objects. That only
        # works because Node defines __lt__ (see tree_node.py), which compares
        # nodes by frequency. Without __lt__, Python would raise a TypeError.
        #
        # Ties: we use strict "<", so when two nodes have the same frequency
        # the one that appears EARLIER in the list wins. Different tie-breaking
        # rules produce different (but equally good) Huffman trees. That is why
        # two correct Huffman implementations can produce different codes for
        # the same message -- yet the total encoded length is the same.
        #
        # Assume the smallest frequency is in the first node
        lowest_idx: int = 0
        for i in range(1, len(self.__forest)):
            # Consider the remaininig nodes
            if self.__forest[i] < self.__forest[lowest_idx]:
                # The current node's frequency is lower than the lowest
                # we have seen so far; remember its position.
                lowest_idx = i
        # Remove the list element with the lowest frequency and return it
        return self.__forest.pop(lowest_idx)

    def __huffman_tree(self) -> None:
        """Apply Huffman's technique to convert a forest of single nodes to
        a binary tree"""
        # THE HEART OF THE ALGORITHM. Huffman's algorithm is GREEDY: at every
        # step it makes the locally best choice (merge the two rarest trees)
        # and it can be proven that this leads to an optimal prefix-free code.
        #
        # Intuition: the two rarest trees get pushed one level deeper, i.e.
        # every symbol inside them gets one more bit in its code. If we must
        # make some codes longer, it is cheapest to do it to the symbols we
        # use the least.
        #
        # Small worked example -- message "AAAABBC" -> A:4, B:2, C:1
        #   forest: [A:4, B:2, C:1]
        #   step 1: remove C:1 and B:2, merge into (*:3) -> [A:4, *:3]
        #   step 2: remove *:3 and A:4, merge into (*:7) -> [*:7]   done
        #
        #               (*:7)
        #              0/   \1
        #            (*:3)  A:4         codes:  A = 1
        #           0/   \1                     C = 00
        #          C:1   B:2                    B = 01
        #
        #   Encoded length = 4*1 + 2*2 + 1*2 = 10 bits (vs. 7*8 = 56 in ASCII)
        #
        # Counting: each pass through the loop removes 2 nodes and adds 1,
        # so the forest shrinks by exactly one per pass. Starting from k
        # leaves, we need k - 1 passes, which creates k - 1 internal nodes.
        # The finished tree therefore has 2k - 1 nodes in total.
        #
        # Running time: k - 1 passes, each calling __smallest_node twice at
        # O(k) apiece, gives O(k^2). With k around 100 that is trivial. For
        # very large alphabets we would replace the list with a min-heap
        # (Python's heapq module, which also relies on Node.__lt__), making
        # each removal O(log k) and the whole build O(k log k).
        if self.__verbose:
            print("Building the Huffman tree...")
        # Node counters for debugging
        internal_nodes: int = 0
        # First build the forest
        self.__build_forest()
        # Process the forest until it's down to one tree.
        while len(self.__forest) > 1:
            # Remove the smallest two nodes (based on their frequencies)
            n1: Node = self.__smallest_node()
            n2: Node = self.__smallest_node()
            # Create a new node whose frequency is the sum of frequencies
            # of the nodes we removed.
            # The new node has symbol None: internal nodes never carry a
            # symbol. Its frequency is the total number of times ANY symbol
            # in its subtree appears in the message.
            n12: Node = Node(None, n1.get_frequency() + n2.get_frequency())
            # Make the nodes we removed the left and right children
            # of the new node.
            # Note that every internal node gets BOTH children. A Huffman
            # tree is therefore a "full" binary tree: each node has either
            # 0 or 2 children, never exactly 1.
            n12.set_left(n1)
            n12.set_right(n2)
            # Place the new node back into the forest.
            # It now competes with the remaining nodes in later passes, just
            # like an ordinary leaf with frequency n1 + n2.
            self.__forest.append(n12)
            internal_nodes += 1
        # Update object fields. The root of the Huffman tree is the remaining
        # node of the forest. The default decoder is also the same as the root
        # of the Huffman tree.
        #
        # EDGE CASES to think about:
        #   - Empty message: the forest is empty, so self.__forest[0] raises
        #     an IndexError.
        #   - Message with only ONE distinct symbol (e.g. "aaaa"): the loop
        #     never runs and the root is itself a leaf. The path to it is
        #     the empty string, so every symbol is encoded as "" and the
        #     encoded message is empty -- information is lost. A common fix
        #     is to special-case this and assign the lone symbol the code "0".
        self.__huffman_root = self.__forest[0]
        self.__decoder = self.__huffman_root
        if self.__verbose:
            print(f"Huffman tree built with {internal_nodes:,d} internal nodes.")

    def __build_encoder(self) -> None:
        """Converts the Huffman tree into into key-value pairs for
        fast encoding. In these pairs, symbols are they keys and their
        prefix-free codes are the vlaues."""
        # Why build a dictionary at all? We COULD find each symbol's code by
        # searching the tree every time we see that symbol, but that would
        # repeat the same search hundreds of thousands of times for a book.
        # Instead we walk the tree ONCE, record every leaf's path, and then
        # every lookup during encoding is O(1). This is a classic
        # "precompute once, look up many times" trade-off.
        #
        # Notice the asymmetry: ENCODING uses a dictionary (symbol -> code),
        # but DECODING uses the tree itself (bits -> walk -> symbol). The
        # tree is the natural structure for decoding because we do not know
        # in advance where one code ends and the next begins.
        if self.__verbose:
            print("Building the encoder...")
        # First, build the Huffman tree
        self.__huffman_tree()
        # Initialize the key-value pairs
        self.__encoder = dict()
        # Peform a depth-first traversal of the Huffman tree. We need
        # a stack data structure to store the various stages of the
        # traversals and te correspoding codes up to that point.
        #
        # This is an ITERATIVE depth-first traversal: an explicit Python
        # list plays the role of the call stack that a recursive version
        # would use. The recursive equivalent would look like:
        #
        #     def visit(node, path):
        #         if node.is_leaf():
        #             encoder[node.get_symbol()] = path
        #         else:
        #             visit(node.get_left(),  path + "0")
        #             visit(node.get_right(), path + "1")
        #
        # The trick is that each stack entry carries the node AND the path
        # taken to reach it, so we never need parent pointers to rebuild a
        # code. Every node is pushed and popped exactly once: O(k) work for
        # 2k - 1 nodes (ignoring the cost of building the path strings).
        root = self.__huffman_root
        # Initialize the stack with a tuple of the current node and
        # the code that corresponds to its path from the root.
        stack = [(root, "")]
        # The travesal continues while the are elements to process
        # in the stack
        while len(stack) > 0:
            # Pop the stack and unpack its contents.
            node, path = stack.pop()
            if node.is_leaf():
                # The current node from the stack is a leaf node. Add
                # a key-value pair to the encoder lookup table, with the
                # node's symbol and its path from the root. The path
                # is the symbol's prefix-free code.
                self.__encoder[node.get_symbol()] = path
            else:
                # The current node from the stack is not a leaf node.
                # Add its children to the stack, and update their
                # paths with the appropriate direction.
                # (Since a Huffman tree is full, both checks are always
                # True for an internal node; they are defensive coding.)
                # Order matters slightly: right is pushed last, so it is
                # popped first. The traversal order changes, but the codes
                # do not -- each code depends only on the path, not on when
                # we happen to visit the leaf.
                if node.has_left():
                    stack.append((node.get_left(), path + self.__LEFT))
                if node.has_right():
                    stack.append((node.get_right(), path + self.__RIGHT))
        if self.__verbose:
            print("Encoder built.")

    def __encode(self, message: str) -> None:
        """Finally encode the given message using the prefix free
        codes that correspond to the frequencies of its symbols."""
        # Note the call chain triggered here. Each private method calls the
        # one before it in the pipeline:
        #   __encode -> __build_encoder -> __huffman_tree -> __build_forest
        #            -> __count_frequencies
        # So a single call to encode() runs the entire algorithm.
        self.__message = message
        self.__encoded = ""
        # First build the encoder
        self.__build_encoder()
        if self.__verbose:
            print(f"Encoding a message with {len(self.__message):,d} symbols...")
            # Print a progress line every 1/20th (5%) of the message. max(1, ...)
            # protects against a step of 0 (and a modulo-by-zero crash below)
            # when the message is shorter than 20 symbols.
            progress_step: int = max(
                1, len(self.__message) // self.__PROGRESS_BAR_LENGTH
            )
            progress: int = 0
        # For every symbol in the input message, find its prefix-free
        # code and add it to the encoded message. Typically, we'd update
        # the output string with something like:
        # output += self.__encoder[c]
        # However, this is inefficient in Python because strings are immutable
        # and every update creates a new string. Instead, we can use a list
        # to store the various parts of the output and then join them at the end.
        #
        # To see why this matters: with "+=", the i-th append copies a string
        # that is already about i codes long, so n appends cost roughly
        # 1 + 2 + ... + n = O(n^2) character copies. list.append is O(1)
        # (amortized) and "".join(parts) copies each character exactly once,
        # so the whole loop is O(total length of the output).
        parts: list[str] = []
        for c in self.__message:
            parts.append(self.__encoder[c])
            if self.__verbose:
                progress += 1
                if progress % progress_step == 0:
                    print(f"{100*progress / len(self.__message):3.0f}% complete.")
        # At the end, join the parts to get the final encoded message.
        self.__encoded = "".join(parts)
        if self.__verbose:
            print(f"Message encoded with {len(self.__encoded):,d} symbols.")

    def __decode(self) -> None:
        """Decode a message. The process requires a decoder, which is
        essentially the Huffman tree used to encode the message in the
        first place."""
        # IMPORTANT: decoding must use the SAME tree that was used for
        # encoding. A tree built from a different message (or even the same
        # message with different tie-breaking) assigns different codes, and
        # the output would be gibberish. That is why encode() returns the
        # tree and decode() requires it -- in a real file format, the tree
        # (or the frequency table) is stored in a header next to the data.
        self.__message = ""
        # The decoding starts at the root of the Huffman tree. We then
        # traverse the encoded message using each of its symbols to
        # follow a path in the tree until we reach a leaf node. When we
        # get to the leaf node we extract the decoded symbol and we
        # return to the root of the decoding tree to process the path
        # to the next leaf node.
        #
        # This is where the prefix-free property pays off: the moment we
        # land on a leaf we KNOW the code is complete, because no code
        # continues past a leaf. No separators or lookahead needed.
        #
        # Example with the tree from __huffman_tree ("AAAABBC"):
        #   bits: 1 1 0 1 0 0 ...
        #   1        -> leaf A, emit A, back to root
        #   1        -> leaf A, emit A, back to root
        #   0 1      -> leaf B, emit B, back to root
        #   0 0      -> leaf C, emit C, back to root
        cursor: Node = self.__decoder
        for c in self.__encoded:
            if c == self.__LEFT:
                cursor = cursor.get_left()
            # (These two tests are mutually exclusive, so "elif" would
            # express the intent more clearly and skip one comparison.)
            if c == self.__RIGHT:
                cursor = cursor.get_right()
            if cursor.is_leaf():
                # Review question: __encode deliberately avoids "+=" on
                # strings for performance. This line uses it. What is the
                # cost for a long message, and how would you apply the same
                # list-and-join fix here?
                self.__message += cursor.get_symbol()
                cursor = self.__decoder
        # What happens with bad input? If the bit string is cut short, the
        # loop ends with the cursor stuck partway down the tree and the
        # incomplete final symbol is silently dropped. A robust decoder would
        # check that cursor is back at the root here and report an error.

    # ----------------------
    # User interface methods
    # ----------------------
    # These two public methods are thin wrappers: they store their inputs
    # in the object's fields, call the private method that does the work,
    # and return the result. This keeps the "how" hidden and gives users a
    # small, simple interface: encode(text) and decode(bits, tree).

    def encode(self, message: str) -> tuple[str, Node]:
        """Method accepts a string and compresses it using Huffman encoding.
        The method returns the compressed message and the Huffman tree used
        to encode it."""
        self.__encode(message)
        return self.__encoded, self.__huffman_root

    def decode(self, encoded: str, decoder: Node) -> str:
        """Decodes a message that has been compressed with a Huffman code.
        The method requires the compressed message and the tree that was
        used to compress it."""
        # Because the tree is passed in, decoding does NOT depend on any
        # earlier call to encode(). A brand-new Huffman() object can decode
        # a message as long as it receives the right tree.
        self.__encoded = encoded
        self.__decoder = decoder
        self.__decode()
        return self.__message
