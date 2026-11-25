# Week 14 Activity: From the Huffman Tree to Hashing

Due Wednesday, December 2. This activity replaces our class meeting for Thanksgiving week. It takes about an hour, and most of it is on paper. You turn in one PDF and one Java file.

## Where we are

On 11/18 we built the Huffman tree for `"hello world"` by hand, and on 11/20 we wrote an iterative traversal that reads the codes off it. That traversal uses a "notepad": a bag of `[node, path so far]` pairs that we keep pulling from until it runs dry. I asked you to trace it by hand; this activity is that trace (Part 1).

Before any of that, on 11/16, we counted how often each character occurs in a message with `count_freq` in [`encoding.py`](../week13/encoding.py), and the counts went into a Python `dict`. In Part 2 you write the same counter in Java, but without a dictionary. In Part 3 you think about why that worked, and what breaks when it no longer can. That is where we pick up when we return on Monday, November 30, with **hashing**.

| Part | What | Time | On |
|---|---|---|---|
| 1 | Trace the notepad traversal on the "hello world" tree | 25 min | paper |
| 2 | Count character frequencies in Java | 20 min | computer |
| 3 | From an array of counts to hashing | 15 min | paper |

## What you're given

| File | What it is |
|---|---|
| `huffman_codes.py` | The traversal from 11/20, clean and runnable, on the "hello world" tree from 11/18. It prints the finished codes, nothing more. |
| [`../week13/encoding.py`](../week13/encoding.py) | `count_freq` from 11/16. Reference for Part 2. |
| `FrequencyCounter.java` | `countFrequency` and `printFrequencies` are stubs for you. `main` is complete. |
| `FrequencyCounterTest.java` | Given tests. Do not change it. |

## Part 1: Trace the notepad (25 min, by hand)

Here is the tree, as `huffman_codes.py` builds it. Leaves show `symbol:frequency`; internal nodes show only their frequency.

```text
                          (11)
                   0 /           \ 1
                   (7)             (4)
               0 /     \ 1     0 /     \ 1
               (4)      l:3     (2)       (2)
           0 /    \ 1       0 /  \ 1   0 /  \ 1
           (2)     o:2      ' ':1  w:1  r:1   d:1
       0 /    \ 1
       h:1    e:1
```

The loop in `get_codes`, in words: pull the **last** item off the notepad (`pop()`). If the node has a left child, write `[left, path + "0"]` on the notepad; if it has a right child, write `[right, path + "1"]`. If it is a leaf, record `codes[symbol] = path`. Stop when the notepad is empty.

1. **Copy the tree** onto your paper.
2. **Trace the loop.** Keep a table with one row per pull. Write the notepad with its first item on the left and its last item on the right. Name an internal node by its frequency and path, for example `(4, "00")`; name a leaf by its symbol, for example `(l, "01")`. Here is how it starts:

   | Step | Pulled | Notepad afterwards (first → last) | Codes recorded so far |
   |---|---|---|---|
   | 0 | | `(11, "")` | |
   | 1 | `(11, "")` | `(7, "0")`, `(4, "1")` | |
   | 2 | `(4, "1")` | `(7, "0")`, `(2, "10")`, `(2, "11")` | |
   | 3 | ... | | |

   Then note: what is the largest the notepad ever gets?
3. **Check your answer.** Run `python3 huffman_codes.py`. It prints the dictionary **in the order its entries were recorded**, so it checks both your codes and the order in which you reached the leaves. If you disagree with it, find the step where you went wrong and mark it on your paper rather than erasing it.
4. **Change one thing.** Suppose `notepad.pop()` became `notepad.pop(0)`, which pulls the **first** item instead. Before you run anything, write down your predictions: does the dictionary change? Does the order of its entries change? What is the largest the notepad gets now? (Trace it if you need to; it's a short table.) Then make the change, run it, and compare. In a sentence or two: on 11/20 I said the removal order doesn't matter for this problem. Does it matter for *anything*?

## Part 2: Count frequencies in Java (20 min)

`count_freq` in Python kept a `dict` from characters to counts. In Java we use something more basic: an **array** of 128 `int`s, one slot per [ASCII](https://en.wikipedia.org/wiki/ASCII) character. That works because in Java a `char` is a small whole number: `'a'` is 97, `' '` is 32. So `counts['a']` is the slot `counts[97]`, and it holds the number of a's.

1. **`countFrequency(String message)`.** Walk the message one character at a time and add 1 to that character's slot. A character outside ASCII, such as `é` (233), has no slot: skip it. (What would happen if you didn't? The array was allocated with exactly 128 slots on day one, as we discussed on 11/09.)
2. **`printFrequencies(int[] counts)`.** Print one line for each character that occurs, in ASCII order: the character in single quotes, a space, its count. Skip the zeros. The Javadoc in the file shows the format.
3. Run the tests, then `java FrequencyCounter` and `java FrequencyCounter "now is the winter of"`, and compare with `count_freq` on the same strings in Python.

### Set up and run

```text
javac *.java
java FrequencyCounterTest
java FrequencyCounter
java FrequencyCounter "your own message"
```

Each test line says `ok` or `FAIL`. Most fail on the untouched scaffold; you want all of them to say `ok`.

### Rules (as in week 11)

- Every method that returns a value has **exactly one `return`**. The scaffold already has it; keep it that way.
- Javadoc on every method, before the header. The stubs have theirs; keep them accurate if you change anything.
- No `java.util`: no `HashMap`, no `ArrayList`. The point is the plain array.

## Part 3: From an array to hashing (15 min, short written answers)

These are not graded for being right; they are graded for being yours. Think them through on paper before you look anything up. We start Monday's class from your answers, so this part is most useful done before then.

1. Python's `count_freq` used a `dict`; your Java version used an array of 128 slots. Your array finds a character's count in **one step**, with no searching: no loop, no comparisons, no tree to descend. Why?
2. On 11/16 we considered compressing whole **words** rather than letters. Suppose you want to count the words of a book with an array, the way you just counted characters. Why can't you write `counts["winter"]++`?
3. Invent a rule that turns **any** word into a whole number between 0 and 999. (Hint: you just saw that characters are numbers.) Write your rule down, then apply it, by hand, to `now`, `is`, `the`, `winter`, `of`.
4. Did two of your five words get the same number? If not, can you find two words that **would**? Could any rule avoid this completely, for every word in English? If two words did land in the same slot of your counting array, what would go wrong, and what could you do about it?

## Reading

- [Wikipedia, Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding) — the algorithm from 11/18, with the history (Huffman wrote it as a term paper, to avoid a final exam). Read the introduction and "Basic technique".
- [Oracle tutorial, primitive data types](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html) — `char` and `int`, and why a character can be used as an array index.
- [Oracle tutorial, arrays](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/arrays.html) — declaring, allocating and indexing Java arrays, from 11/09.
- [Wikipedia, ASCII](https://en.wikipedia.org/wiki/ASCII) — the 128 characters your array has slots for. Look at the printable-characters table.
- [Wikipedia, breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) — what Part 1, step 4 turns the traversal into. The first section is enough. *Optional;* you'll see it again in COMP 272 and COMP 363.
- [OpenDSA, introduction to hashing](https://opendsa-server.cs.vt.edu/ODSA/Books/CS3/html/HashIntro.html) — for Monday. **Read it after you write your answers to Part 3**, not before.

Previously assigned readings are still fair game for questions in class or on assessments.

## Turning it in

Upload two files to Sakai by **Wednesday, December 2**:

1. **One PDF** with your Part 1 tree, your trace table, the largest notepad size, your predictions and results for step 4, and your answers to Part 3. Phone photos are fine, as long as they are in order, right side up, and readable.
2. **`FrequencyCounter.java`.** Run the tests before you upload, and do not edit `FrequencyCounterTest.java`.
