# Week 7 Assignment: The Mystery Sorters

## The task

This week we talked about why sorting matters — a sorted collection
lets you search it dramatically faster — and looked at how sorting
costs grow: linear, $n \log n$, quadratic, and worse than any of those.
This assignment gives you three "mystery" sorting functions —
`gandalf`, `saruman`, and `sauron` — and asks you to figure out, purely
from *timing* them, what each one is actually doing underneath.

All three share one contract:

```python
def mystery_sort(a: list[int]) -> list[int]:
    ...
```

Each takes a list of integers and returns a **new**, sorted list. None
of them modifies the list you pass in. That's all you're told.

**Do not read the package's source to answer this assignment.** Yes,
it's an installable package, so nothing physically stops you from
downloading and opening it — but doing that defeats the point of the
exercise, which is to reason from behavior the same way you'd have to
with any library you didn't write and can't inspect.

## Setup

```
pip install comp271-mystery-sorters
```

```python
from comp271_mystery_sorters import gandalf, saruman, sauron
```

## What to turn in

A short write-up (code + text, however you want to present it) covering:

1. **How you timed each function.** Use `time.perf_counter()`, not
   `time.time()`. For each timing, generate a **fresh random list**
   and time one call; repeat several times (5 is reasonable) with a
   new random list each time, and average the results. One run is a
   sample, not a measurement.

2. **Work through one function at a time — don't test all three
   against one shared list of sizes.** For each function, in turn:

   - Start at $n = 16$.
   - Time it (averaged as above).
   - **Add 1 or 2 to $n$** — your choice, but stay consistent for that
     function — and time it again. Keep adding the same amount each
     step: $16, 18, 20, 22, \ldots$ or $16, 17, 18, 19, \ldots$. Do
     **not** double $n$.
   - Keep stepping and recording until **either**:
     - a single call takes uncomfortably long by your own standard
       (5–10 seconds is reasonable), **or**
     - you've spent more than a time budget you set for yourself on
       this one function overall (60–90 seconds of total wall-clock
       time, across every step so far) — **whichever happens first.**
   - Drop the function the moment either line is crossed: stop testing
     it, record your last size and time, and move on. Only then move to
     the next function, starting over at $n = 16$.

   **Why two stopping rules, not just one:** with small additive steps,
   a slow function doesn't suddenly take 10 seconds on one call — each
   step is only a little slower than the last. What adds up is the
   *total* time spent taking hundreds or thousands of small steps. Watch
   the clock on the whole experiment, not just on each individual call,
   or a slow function can quietly run for a very long time without any
   single call ever looking alarming.

   You will likely **not** reach the same $n$ for every function — the
   function that's growing faster will cross your time budget at a
   smaller $n$ than one that's growing slower. That difference is itself
   a data point, not a nuisance: mention it in item 4.

3. **Your data.** Stepping by 1 or 2 from $n=16$, you'll collect far
   more points than a doubling approach would — likely hundreds to low
   thousands per function. Don't try to type them all into a table.
   - A **plot** (average time vs. $n$, one line per function) is the
     right tool here — the shape of the curve is what you're looking for.
   - If you'd rather use a table, report a **sampled subset** (every
     25th or 50th point, say) plus your first and last point.
   - Either way, state your trial count, your chosen increment (1 or
     2), both stopping thresholds, and the size you stopped at for each
     function.

4. **Your conclusion, with reasoning.** For each function, name the
   growth class you believe it falls into — $\Theta(n)$,
   $\Theta(n \log n)$, $\Theta(n^2)$, or "worse than any polynomial
   we've discussed" — and, if you're willing to commit, which specific
   algorithm (or something not covered in class at all) you think it
   is.

   Since adjacent additive steps barely differ, don't compare adjacent
   rows the way you would with doublings. Instead, pick two points far
   apart in your own data (your first and last, say) and estimate a
   growth exponent: if time scales as $n^k$, then $k \approx
   \log(t_2/t_1) / \log(n_2/n_1)$. A $k$ near 1 suggests linear, near 2
   suggests quadratic. You can also just describe the plotted shape —
   straight line, gentle curve, sharply bending curve — as long as you
   point to what you actually saw. **Cite your own numbers or your own
   plot.** "It felt slow" isn't an argument; "I estimated $k \approx
   1.9$ from my first and last points" or "the curve bends upward
   noticeably, unlike the other two functions" is. A wrong guess at the
   specific algorithm with solid reasoning from the data earns more
   credit than a right guess with no numbers behind it.

## Reading (preview for next week)

Estimating $k$ above is really estimating a logarithm, and next week's
material is built on logarithms directly — get a head start now:

- [Villarreal-Calderon, "Chopping Logs: A Look at the History and Uses of Logarithms"](../oer/A%20Look%20at%20the%20History%20and%20Uses%20of%20Logarithms.pdf) (*The Mathematics Enthusiast*, 2008) — Napier's 1614 invention and his own stated motivation, Briggs's common-log tables, the slide rule, and the natural logarithm's calculus roots, in one piece.
- [Wikipedia, "History of logarithms"](https://en.wikipedia.org/wiki/History_of_logarithms) — a complementary, more encyclopedic account of the same history.
