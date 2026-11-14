# Week 12 Assignment — In-Order Traversal, by Hand

Due Friday, November 20. You turn in one PDF: scans or photos of your hand-written traces.

## Where we are

Deleting a node with two children comes down to one move: swap its value with its **in-order predecessor** (the rightmost node of its left subtree), then delete that node, which has at most one child. The predecessor is simply the node that comes right before the target when the tree is read **in order**. And reading a binary search tree in order produces its values in ascending order.

That makes in-order traversal the one idea from this course worth carrying out the door. We wrote it two ways on 11/13:

- **Recursive.** If the node is not empty: traverse its left subtree, process the node, traverse its right subtree. The computer's call stack remembers where to come back to.
- **Iterative.** The same walk, but we keep the stack ourselves: go left as far as you can, pushing each node you pass; pop, process, and go right.

[`inorder_traversal.py`](./inorder_traversal.py) is clean, runnable code for both, in Python. Treat the code on the slides as pseudocode. This file is the version that runs.

## The task

Trace **both** versions **by hand**, on paper, on each of these three trees. Build each tree by inserting the numbers, in the order given, into an empty binary search tree.

| Tree | Insert, in this order |
|---|---|
| A (the tree from class on 11/13) | 50, 40, 60, 45, 55 |
| B | 40, 30, 20, 10 |
| C | 10, 20, 30, 40 |

For each tree:

1. **Draw the tree.**
2. **Trace the recursive version.** Write down every call, indented one level deeper for each call it makes, including the calls on an empty subtree, and mark the moment each node is processed. Here is how Tree A starts:

   ```text
   in_order(50)
       in_order(40)
           in_order(None)      nothing to do
           process 40
           in_order(45)
               ...
   ```

   Then note: what is the largest number of calls that are **parked** (started, but not finished) at the same moment?
3. **Trace the iterative version.** Keep a table with one row for every push and every pop. Write the stack with its bottom on the left. Here is how Tree A starts:

   | Step | Action | `current` afterwards | Stack (bottom → top) | Processed so far |
   |---|---|---|---|---|
   | 1 | push 50, go left | 40 | 50 | |
   | 2 | push 40, go left | None | 50, 40 | |
   | 3 | ... | | | |

   Then note: what is the largest the stack ever gets?
4. **Check your answer.** Run `inorder_traversal.py`. It prints the order in which each tree's nodes are processed, nothing more. If your trace ends in a different order, find the step where you went wrong, and mark it on your paper rather than erasing it.

Then answer, in a few sentences, at the end of your traces:

5. Trees B and C hold the same four numbers. Compare the numbers you wrote down in steps 2 and 3 for B and for C. For which version does the shape of the tree change the answer, and for which doesn't it? Why?
6. On 11/13 I said the recursive version is elegant but hard on memory for large trees, and the iterative one is kinder. Using your answers for B and C, what kind of tree, of say a million nodes, would make that difference matter? What kind would not?

## Rules

- **The traces are by hand.** Do not copy a computer printout into your own handwriting: that shows you can copy, which I already believe. The program gives you only the final order, so you can check your answer. The steps in between are yours.
- Show every step, including the calls on empty subtrees and the pops. Skipping "obvious" steps is how traces go wrong.
- Neat is not required. Legible is.

## Reading

- [Class slides, 11/13: deleting nodes and in-order traversal](https://docs.google.com/presentation/d/1jB63HV7vz7VftcZbO7ZYYQBToW8YTzyw8ho8c0yx2Rg/edit?usp=sharing) — the three deletion cases, the in-order predecessor and successor, and both traversals. The code on the slides is pseudocode; [`inorder_traversal.py`](./inorder_traversal.py) is the version that runs.
- [OpenDSA, preorder, postorder, and in-order traversals](https://opendsa-server.cs.vt.edu/ODSA/Books/CS3/html/BinaryTreeTraversal.html) — the three traversal orders, with step-through visualizations. Run the in-order one and watch the order change.
- [Wikipedia, tree traversal: in-order and its implementations](https://en.wikipedia.org/wiki/Tree_traversal#In-order,_LNR) — the in-order definition, then the recursive and iterative versions under "Implementations", which match ours.
- [Wikipedia, deleting from a binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree#Deletion) — the three deletion cases from 11/11 and 11/13, including the swap with the predecessor or successor.
- [Wikipedia, the call stack that recursion relies on](https://en.wikipedia.org/wiki/Call_stack) — where the parked calls in your recursive trace actually live. Read the first two sections. *Optional.*
- [Wikipedia, the Kobayashi Maru: Star Trek's unwinnable test](https://en.wikipedia.org/wiki/Kobayashi_Maru) — the test Kirk passed by changing the rules, as we did for two-child deletion. No 500-page essay required. *Optional.*

Previously assigned readings are still fair game for questions in class or on assessments.

## Turning it in

Upload a single PDF to Sakai with, for each of trees A, B and C: the drawing, the recursive trace, the iterative table, and the two numbers from steps 2 and 3. Put your answers to questions 5 and 6 at the end. Phone photos are fine, as long as they are in order, right side up, and readable.
