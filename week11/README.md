# Week 11 Assignment — Searching a Binary Search Tree, in Java

Due Friday, November 13. You turn in two files: `BinarySearchTree.java` and `Node.java`.

## The task

In class we built a binary search tree of strings in Python, and then rebuilt `Node` and `insert` in Java. This week you write the missing piece **in Java yourself**, and then change what the tree does with duplicates.

- **Part A. `search`.** Write `public boolean search(String value)` and its private recursive helper `searchRec`. The Python version is in [`bst.py`](./bst.py), in both flavors we pseudocoded (recursive on 11/2, iterative on 11/4). Read it, then write the Java.
- **Part B. Frequency.** Until now the tree has skipped duplicates: inserting `"the"` a second time does nothing. Change it to **count** them instead. How the tree remembers repeats is for you to design; the tree must then answer `frequency(String value)`.

The point is practice writing Java. I assume no prior Java; the goal is working code, not award-winning code.

## What you're given

| File | What it is |
|---|---|
| `Node.java` | The class from Friday, unchanged. |
| `BinarySearchTree.java` | `insert` and `insertRec` are complete (and fixed). `search`, `searchRec` and `frequency` are stubs for you; one `else` branch in `insertRec` is marked **PART B**. |
| `BinarySearchTreeTest.java` | Given tests. Do not change it. |
| `bst.py` | The Python tree, with working `search`. Reference only. |

**A fix to `insertRec`.** The version we posted on Friday had the bug from the Python class on 10/28: it wrote `currentNode = insertRec(currentNode.getLeft(), newNode)`, so after the second insert the tree forgot its root. The files in this folder are updated: `insertRec` now re-attaches the result with `currentNode.setLeft(...)` and `currentNode.setRight(...)` and leaves `currentNode` alone. Pull the updated `BinarySearchTree.java` and `Node.java` and work from them; discard your Friday copies.

## Part A — `search`

`public boolean search(String value)` returns `true` if `value` is in the tree and `false` otherwise.

1. The public method wraps the string in a `Node`, as `insert` does, and starts the recursion at the root.
2. The private helper takes the node it is looking at and the target. There are two base cases: an empty subtree (`null`) means the value is **not** in the tree; a node that is neither smaller nor larger than the target (`compareTo` returns `0`) means it **is**. Otherwise search the left or the right subtree.
3. Compare nodes with `compareTo`. Do not write your own string comparison.

Before you code, trace by hand: insert `now is the winter of` into an empty tree, draw the tree, and follow `search("of")` and `search("moon")` from the root. Write down which nodes you visited.

*Optional:* write `searchIterative` too, the `while` version from 11/4. If you do, it is `public boolean searchIterative(String value)` in the same class.

## Part B — Count instead of skip

1. Change the tree so a value inserted more than once is **counted**, not skipped. Where the count lives, and which classes and methods you change to hold it, is your design. `size` still counts **distinct** values, so inserting a repeat must not change it. Fields stay `private`.
2. Write `public int frequency(String value)`: the number of times `value` was inserted, or `0` if it never was.
3. Answer in a comment at the top of `BinarySearchTree.java`: how does your design record a repeat, and what did you change in `Node` and in `insertRec` to make it work? Which Python line would the same idea change?

## Rules

- Every method that returns a value has **exactly one `return`**. Set a pessimistic default and overwrite it.
- Javadoc comment on every method you write, placed **before** the header, with `@param` and `@return`.
- Fields stay `private`. Use the getters and setters (`getLeft()`, not `.left`).
- No `java.util` collections and no libraries for the tree itself.

## Set up and run

You need a working Java environment (Codespaces, or a JDK with VS Code). Check it first:

```text
javac -version
java -version
```

Then, in the folder with the files:

```text
javac *.java
java BinarySearchTreeTest
```

Each line says `ok` or `FAIL`. Some tests fail on the untouched scaffold; you want all of them to say `ok` when you finish. Also try the Python version with your own words and compare the answers.

## Reading

- [OpenDSA, binary search tree operations](https://opendsa-server.cs.vt.edu/ODSA/Books/CS3/html/BST.html) — definition, insert, remove, and analysis of the BST (section 7.11); the search we write follows the same descent as insert.
- [Oracle, learning the Java language](https://docs.oracle.com/javase/tutorial/java/index.html) — the official Java tutorial trail: syntax, classes, and objects. Skim what you need for the Java you write.
- [Java `Comparable` interface contract](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Comparable.html) — what `compareTo` promises, and why `0` means "equal".
- [Java `String` `compareTo` method](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html#compareTo(java.lang.String)) — how our nodes order words.
- [Wikipedia, searching and inserting in trees](https://en.wikipedia.org/wiki/Binary_search_tree) — the search and insertion operations, and why balance matters.
- [Oracle tutorial, the while statement](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/while.html) — for the optional iterative search.
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) — naming and formatting, for the style questions we discussed on 11/6.

## Thanksgiving week: tell me what you prefer

We do not meet on Wednesday or Friday of Thanksgiving week. The Monday before, **November 23**, is up to you: in person, on Zoom, or asynchronous (no meeting, with a reading or activity to do on your own). Please answer the one-question survey:

[Thanksgiving Monday survey: in person, Zoom, or asynchronous](https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=408fApwrJEiDeLvPnsWsy7I196tvCVFAgylhP23oZuNUMVFFT1BHNlAwRTROOVBFUUU1TTFLUENGVy4u)

If I hear nothing, we meet in person as planned.

## Turning it in

Upload `BinarySearchTree.java` and `Node.java` to Sakai. Run the tests before you upload and do not edit `BinarySearchTreeTest.java`.
