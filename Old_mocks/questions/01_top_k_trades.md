# Mock 1 — Top K Trades

This mirrors the most consistently reported question shape for this round. Play it as a
live progression — don't jump ahead to later parts before finishing the current one the way
an interviewer would actually reveal it.

## Part 1 — set the scene, as the interviewer would say it
> "Here's a list of trade sizes that came in today: `[40, 10, 90, 30, 90, 5]`. Write me a
> function that finds the largest one."

Before writing anything: what, if anything, would you ask? (Think of at least one question
before moving on — see the answer key for what's worth clarifying and why.)

Write `largest(trades)`.

## Part 2 — the actual reported ask
> "Now find the three largest."

Write `top_three(trades)` returning the three largest values, in descending order.

Think about, and be ready to state out loud:
- What should happen if there are duplicate values among the top three (e.g. two trades of
  size 90)? Do they both count?
- What should happen if there are fewer than 3 trades total?
- What's the time complexity of your solution? Could it be done without sorting the *entire*
  list?

## Part 3 — the generalization
> "Good. Now generalize that to the k largest, for any k."

Write `top_k(trades, k)`.

Follow-up to be ready for out loud: is your solution still doing more work than necessary if
`k` is small (say 3) but the input list is huge (say a million trades)? What would you change,
even just describing it verbally without full code, to avoid sorting all million?

## Part 4 — the streaming twist
> "One more thing — suppose trades don't all arrive up front. They come in one at a time,
> throughout the day, and at any point someone might ask 'what are the current top k trades
> so far?' How would your approach change?"

No code required for this part — a clear verbal answer describing the data structure and
update rule you'd use, and why, is the actual ask.

## Part 5 — manual trace (do this even if you have a Python interpreter open)
Take whatever `top_k` you wrote and trace it by hand, writing down intermediate state, for:
```
top_k([40, 10, 90, 30, 90, 5], 3)
```
Then trace it for the edge case:
```
top_k([7], 5)
```
Do this on paper or in a plain text file — not by running it — and only then check it against
Python.

---

## Part 6 — the reported constraints (added from candidate reports)
Two specific versions of this question were reported. Do both.

### 6a — "without using a helper function"
> "Given a list of trades, find the top 3 — **without using a helper function**."

That means no `sorted()`, no `max()`, no `heapq`. Track the top three in variables yourself
in a single pass. Handle: fewer than 3 elements, duplicates, all-negative values.

### 6b — "what if the trades contain long and short sells?"
> "What if the trades contain long and short sells?"

Now quantities are **signed** — a short is negative. Before coding, ask the question this is
really testing: **does "top 3 trades" mean the three largest signed values, or the three
largest by absolute size?** Argue for magnitude (a -250 short is a bigger trade than a +100
long) but confirm rather than assume. Then handle it.
