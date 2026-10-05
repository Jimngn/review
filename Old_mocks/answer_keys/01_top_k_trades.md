# Answer Key — Mock 1 (Top K Trades)

## Part 1 — largest single value
Worth asking before coding (this is the kind of thing that reportedly matters as much as the
code itself): "Can the list be empty? Are trade sizes always positive?" There's no single
right clarifying question — the point is that you ask *something* rather than silently
assuming.
```python
def largest(trades):
    if not trades:
        return None          # or raise, depending on what you agreed with the interviewer
    best = trades[0]
    for x in trades[1:]:
        if x > best:
            best = x
    return best
```
This is `max(trades)` under the hood — writing it manually shows you understand *how* it
works (single pass, track the best seen so far), which is exactly what a "walk me through
your reasoning" round wants to see, even though `max()` itself would be a perfectly
acceptable one-line answer if that's all that was asked.

## Part 2 — top three
**Simplest correct answer** (state the complexity honestly, then optionally improve it):
```python
def top_three(trades):
    return sorted(trades, reverse=True)[:3]
```
Complexity: O(n log n) for the sort, O(1)-ish beyond that. For `[40, 10, 90, 30, 90, 5]`
this gives `[90, 90, 40]` — duplicates (two 90s) are both kept, since the problem never said
values had to be distinct, only "the three largest values". If there are fewer than 3 trades,
slicing past the end (`[:3]` on a 2-element list) just returns what's there — no crash, no
special-case code needed.

**The O(n), O(1)-extra-space version** (this is very likely the actual target, given the
"constant time/space" detail in the report — for a *fixed* k=3, you don't need to sort
anything, you just need 3 tracking variables):
```python
def top_three(trades):
    top = [float("-inf"), float("-inf"), float("-inf")]   # top[0] >= top[1] >= top[2]
    for x in trades:
        if x > top[0]:
            top = [x, top[0], top[1]]
        elif x > top[1]:
            top = [top[0], x, top[1]]
        elif x > top[2]:
            top = [top[0], top[1], x]
    return top
```
One pass over the data (O(n)), only ever holding 3 numbers regardless of input size (O(1)
extra space) — this is the version to lead with if the interviewer pushes on "can you avoid
sorting everything," and it directly demonstrates the fixed-k-vs-full-sort trade-off they
seem to be probing for. Trace it by hand on the example before presenting it as done — it's
easy to get an off-by-one in the shifting logic (which slot moves where).

## Part 3 — generalize to top k
For arbitrary `k`, the fixed-3-variable trick doesn't scale cleanly, so falling back to
sorting is a completely reasonable answer — just say so explicitly:
```python
def top_k(trades, k):
    return sorted(trades, reverse=True)[:k]
```
If pushed on efficiency for "large input, small k": the right *concept* to name is a
**min-heap of size k**. Walk through it verbally even if you don't produce full code:
process each element once; keep a heap holding the current best k seen so far; if a new
value beats the smallest thing currently in the heap, it replaces it. Each of the n elements
costs O(log k) to process, giving O(n log k) total — better than O(n log n) when k is much
smaller than n. If you do want to write it:
```python
import heapq

def top_k(trades, k):
    return heapq.nlargest(k, trades)
```
`heapq.nlargest` does exactly the min-heap-of-size-k approach internally. Naming the
approach out loud is worth more here than reciting the exact `heapq` API from memory — if
you forget the function name, describing the mechanism is a perfectly good fallback.

## Part 4 — streaming follow-up (verbal)
Key idea: maintain a min-heap of size k as your running state, seeded as trades arrive
during the day.
- On each new trade `x`: if the heap has fewer than k elements, add it. Otherwise, compare
  `x` to the smallest element currently in the heap (the heap's root) — if `x` is larger,
  pop the smallest and push `x`; otherwise ignore `x` (it's not in the current top k).
- "What are the top k so far?" is answered by reading out the heap's contents at any time —
  O(k) to sort/display, O(log k) to update per new trade.
- Contrast this explicitly with the batch approach: re-sorting the whole list every time a
  new trade comes in would be extremely wasteful; a heap gives you incremental updates.

## Part 5 — manual trace
For `top_k([40, 10, 90, 30, 90, 5], 3)` using `sorted(..., reverse=True)[:3]`:
sorted descending: `[90, 90, 40, 30, 10, 5]` -> take first 3 -> `[90, 90, 40]`.

For `top_k([7], 5)`: sorted descending: `[7]` -> `[:5]` on a 1-element list just returns
`[7]` — no error, because Python slices never raise for an out-of-range stop index.

---

## Part 6 — the reported constraints

### 6a — no helper functions (verified)
```python
def top_three(trades):
    a = b = c = None
    for x in trades:
        if   a is None or x > a: a, b, c = x, a, b
        elif b is None or x > b: b, c = x, b
        elif c is None or x > c: c = x
    return [v for v in (a, b, c) if v is not None]
```
Verified: `[40,10,90,30,90,5]` → `[90, 90, 40]`; `[7]` → `[7]`; `[]` → `[]`;
`[5,5,5,5]` → `[5,5,5]`; `[-3,-1,-2]` → `[-1,-2,-3]`.

Two things to say while writing it:
- **Use `None`, not `0` or `-1`, as the initial sentinel.** With `0`, an all-negative input
  returns zeros that were never in the list — a silent wrong answer. `float("-inf")` also
  works but then you must filter it out of the result for short inputs.
- The tuple assignment `a, b, c = x, a, b` shifts everything down in one step. Written as
  three separate statements in the wrong order you'd clobber `b` before saving it — a classic
  live-coding bug. Narrate that you're doing it simultaneously on purpose.

O(n) time, O(1) space, one pass. State that unprompted.

### 6b — long and short sells (verified)
**Ask first**: largest signed, or largest by absolute size? Make the case for magnitude —
*"a 250-lot short is a bigger trade than a 100-lot long; if we're ranking by trade size,
direction shouldn't shrink it"* — then confirm. If they want signed, it's your Part 2 code
unchanged, and saying so is fine.

For magnitude, keeping the symbol attached:
```python
def top3_by_size(trades):            # trades: [(symbol, signed_qty), ...]
    best = []
    for t in trades:
        best.append(t)
        i = len(best) - 1
        while i > 0 and abs(best[i][1]) > abs(best[i-1][1]):
            best[i], best[i-1] = best[i-1], best[i]
            i -= 1
        if len(best) > 3:
            best.pop()
    return best
```
Verified: `[("AAPL",100),("MSFT",-250),("GOOG",50),("TSLA",-10),("NVDA",200)]` →
`[("MSFT",-250), ("NVDA",200), ("AAPL",100)]`.

Insertion into a bounded list keeps it O(n) with O(1) space (the inner loop runs at most 3
times). **Return the signed value, not the absolute one** — you rank by magnitude but report
reality; dropping the sign would hide whether the desk is long or short.

Edge cases to raise: a quantity of exactly 0; a long and a short of equal magnitude (which
ranks first, and does it matter?); whether a "trade" should be ranked by quantity or by
notional (quantity × price), which is usually the more meaningful business answer and is
worth asking about.
