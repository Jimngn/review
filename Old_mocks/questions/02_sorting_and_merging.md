# Mock 2 — Sorting and Merging

One report described this round as "live coding about sorting algorithms" done directly with
a team member. You almost certainly won't be asked to implement quicksort from memory under
pressure — but you should be able to implement *a* simple sort by hand, explain its
complexity, and use sorting as a building block, since Python's built-in `sorted()` alone
sidesteps the actual skill being tested (can you reason about ordering things and combining
ordered things).

## Part 1
> "Without using Python's built-in `sorted()` or `.sort()`, write a function that sorts a
> list of numbers in ascending order."

Pick any algorithm you can actually explain clearly — selection sort or insertion sort are
both fine and simple to reason about live; you do not need the fastest algorithm, you need
one you can implement correctly and narrate. Write `my_sort(nums)`.

Be ready to state, out loud, without looking it up:
- What's the time complexity of the algorithm you picked, and why?
- Does it work correctly on an empty list? A single-element list? A list with duplicates?

## Part 2
> "Now here's a different scenario: you have two lists that are each *already* sorted, and
> you want to combine them into one sorted list. Can you do that without just concatenating
> them and re-sorting from scratch?"

Write `merge_sorted(a, b)`.

Follow-up: why is this approach faster than concatenating and calling your Part 1 sort (or
`sorted()`) on the combined list? Be able to state both complexities and explain the gap in
plain language, not just cite the Big-O notation.

## Part 3
> "Suppose instead of two lists, you have a *list of* several already-sorted lists — say,
> trade logs from several different desks, each individually sorted by time, and you need
> one combined sorted log. How would you extend what you just wrote?"

No full implementation required — describe the approach out loud first (repeatedly applying
your two-list merge is a completely valid answer), and write code only if there's time or
you're asked to.

## Part 4 — manual trace
Trace your `merge_sorted` function by hand, step by step, for:
```
merge_sorted([2, 5, 8], [1, 3, 9, 10])
```
Write out the state of both pointers and the result list after every step, without running
the code.

---

## Part 4 — the reported version (added from candidate reports)
> "Code an **O(n) complexity** sorting algorithm for a **short array**."

Reported almost verbatim. Think before you object: comparison-based sorting has a proven
O(n log n) lower bound, so an O(n) sort must **not be comparison-based** — which means it
needs an extra assumption about the data.

Ask the question that unlocks it: **"What's the range of values?"** The phrase "short array"
is doing work here — it hints the values are small, bounded integers.

Write it. Then be ready for:
- What's the actual complexity, stated honestly? (It is not simply O(n).)
- When is this *worse* than just calling `sorted()`?
- What breaks if the values are floats? Negative? Arbitrary strings?
- Is your version stable, and why would anyone care?
