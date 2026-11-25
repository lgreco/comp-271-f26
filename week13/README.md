
# Huffman app in Python

[Class `Huffman`](./huffman.py) in this repo implements a Huffman encoder. I have added some code to allow verbose or silent execution, showing the steps during runtime.  The code follows the schematic below:


<center>

![](https://raw.githubusercontent.com/lgreco/images/refs/heads/main/huffman/huffman_encoder.png)

---

![](https://raw.githubusercontent.com/lgreco/images/refs/heads/main/huffman/huffman_decoder.png)


</center>

## What's in this folder

| File | What it is |
|---|---|
| [`encoding.py`](./encoding.py) | `count_freq`, the character counter from 11/16. It is step 1 of the encoder, on its own. |
| [`tree_node.py`](./tree_node.py) | Class `Node`, the binary tree node. A leaf holds a symbol and its frequency; an internal node holds only the sum of its children's frequencies. |
| [`huffman.py`](./huffman.py) | Class `Huffman`, the full encoder and decoder. Its public methods are `encode` and `decode`; everything else is private. |
| [`test_huffman.py`](./test_huffman.py) | A script that downloads a book from Project Gutenberg, compresses it and reports how much space we saved. |

The code is commented heavily for review. Read the comments along with the code; they explain *why* each step works, not only what it does.

## Running it

The test script needs two packages that are not part of standard Python, and an internet connection to fetch the book:

```bash
python -m pip install requests pympler
cd week13
python test_huffman.py
```

Run it from inside `week13`, because `huffman.py` imports `tree_node` from the same folder. With `verbose=True` (as in the script) you see each step of the schematic as it happens: how many unique symbols, how many nodes in the forest, how many internal nodes in the tree, and the progress of the encoding.

To try it on your own text, from inside `week13`:

```python
from huffman import Huffman

h = Huffman()                       # Huffman(verbose=True) to see the steps
encoded, tree = h.encode("AAAABBC")
print(encoded)                      # 1111010100
print(h.decode(encoded, tree))      # AAAABBC
```

## How the code maps to the schematic

A single call to `encode` runs the whole encoder. Each private method calls the one before it, so the steps happen in this order:

| Step | Method | What it does |
|---|---|---|
| 1 | `__count_frequencies` | Counts how many times each symbol appears. Same as `count_freq` in `encoding.py`. |
| 2 | `__build_forest` | Turns each symbol and its count into a one-node tree (a leaf). The list of leaves is the **forest**. |
| 3 | `__huffman_tree` | Repeatedly removes the two nodes with the **smallest** frequencies, makes them the children of a new node, and puts the new node back. When one node is left, it is the root of the Huffman tree. |
| 4 | `__build_encoder` | Walks the tree once and records each leaf's path from the root, with left = `0` and right = `1`. That path is the symbol's code. The walk uses a stack of `(node, path so far)` pairs: the "notepad" from 11/20. |
| 5 | `__encode` | Replaces each symbol of the message with its code. |

Decoding (`decode` and `__decode`) goes the other way. Start at the root, follow one bit at a time (left on `0`, right on `1`), and when you land on a leaf, write down its symbol and go back to the root.

### A small example

For `"AAAABBC"` the counts are A:4, B:2, C:1. The two smallest are C and B, merged into a node of frequency 3. Then that node and A are merged into the root, with frequency 7:

```text
            (7)
         0 /   \ 1
         (3)    A:4         A = 1
      0 /   \ 1             B = 01
     C:1    B:2             C = 00
```

The encoded message is `1 1 1 1 01 01 00`, which is **10 bits**. In 8-bit ASCII the same seven characters take 56 bits.

## Ideas to hold on to

- **Frequent symbols get short codes; rare ones get long codes.** That is the entire source of the savings.
- **Symbols live only in the leaves.** So no code can be the beginning of another code (the codes are **prefix-free**). That is why the decoder knows a code is finished the moment it reaches a leaf, with no separators between codes.
- **The decoder needs the same tree that the encoder used.** That is why `encode` returns the tree along with the bits. In a real compressed file, the information needed to rebuild the tree is stored at the front of the file.
- **The `"0"`/`"1"` here are characters, not bits.** We count each one as a bit when we measure compression; a real compressor packs eight of them into one byte.

## Questions for review

1. Build the Huffman tree for `"hello world"` by hand, as we did on 11/18. Then run `Huffman().encode("hello world")`. Are the codes the same as yours? If not, is the total number of bits the same? Why can two correct trees differ?
2. `__smallest_node` scans the whole forest every time it is called. With *k* unique symbols, how many times is it called in total, and what is the overall running time of building the tree? Why does that hardly matter for English text?
3. What happens if you encode `"aaaa"`, a message with only one distinct symbol? Try it, then decode the result. What went wrong, and how would you fix it?
4. `__encode` collects the codes in a list and joins them at the end, instead of using `+=` on a string. `__decode` uses `+=`. Why is the list faster, and how would you change `__decode`?
5. `test_huffman.py` never checks that decoding gives back the original book. Uncomment the round-trip check at the bottom of the script and run it.
6. Switch `source` to `short_book` in `test_huffman.py`. Before you run it, predict: does the compression ratio go up or down? Why does the size of the tree matter more for a short message?
