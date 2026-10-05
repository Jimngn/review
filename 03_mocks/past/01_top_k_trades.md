# PAST QUESTION: Top 3 Trades → Top K → Streaming

**This was asked in your previous technical round.** Final rounds often reuse the same
*shape* with a new twist, so redo it cold. Write it in a txt file, don't run it, and trace by
hand.

---

## The question (as it unfolds)

**Part 1.**
> "Here are today's trade sizes: `[40, 10, 90, 30, 90, 5]`. Return the 3 largest."

**Part 2.**
> "Can you do it in one pass, without sorting and without helper functions like `sorted`,
> `max`, or `heapq`?"

**Part 3.**
> "Now generalize to the top **k**."

**Part 4.**
> "Trades now arrive **continuously** all day. At any moment someone can ask 'what are the
> top k so far?' What changes?"

**Twists that have been reported:**
- "What if the trades contain long **and short** sells?" (signed quantities)
- "What if each trade is `(symbol, qty)` and you need to return the symbol too?"

Before scrolling: clarifying questions? Duplicates? Fewer than 3 trades? Empty list?
Negative numbers?

<br><br><br><br><br><br><br><br><br><br>

---
---

## ANSWERS

### Clarifying questions worth asking
- Do duplicates count separately? (Usually yes: two 90-lot trades are two trades.)
- What if there are fewer than 3 trades? (Return what you have.)
- Can sizes be negative / are shorts negative? (Leads to the twist.)
- Return values in descending order?

### Part 1: simplest correct
```python
def top_three(trades):
    return sorted(trades, reverse=True)[:3]
```
O(n log n). Slicing past the end is safe: `[7][:3]` → `[7]`. Say the complexity, then offer
the faster version.

### Part 2: one pass, no helpers
```python
def top_three_one_pass(trades):
    a = None    # largest
    b = None    # 2nd
    c = None    # 3rd
    for x in trades:
        if a is None or x > a:
            a, b, c = x, a, b          # everyone shifts down
        elif b is None or x > b:
            b, c = x, b
        elif c is None or x > c:
            c = x
    result = []
    for v in [a, b, c]:
        if v is not None:
            result.append(v)
    return result
```
Trace `[40, 10, 90, 30, 90, 5]`:
| x | a | b | c |
|---|---|---|---|
| 40 | 40 | None | None |
| 10 | 40 | 10 | None |
| 90 | 90 | 40 | 10 |
| 30 | 90 | 40 | 30 |
| 90 | 90 | 90 | 40 |
| 5 | 90 | 90 | 40 |
→ `[90, 90, 40]` ✓

Two things to say out loud:
- **`None` as the starting value, not 0.** With 0, `[-3, -1, -2]` would wrongly return
  zeros that were never in the list.
- **`a, b, c = x, a, b` happens all at once.** Writing `b = a` then `c = b` in separate lines
  would copy the wrong value. Classic no-run bug.

O(n) time, O(1) extra space.

### Part 3: top k
```python
def top_k(trades, k):
    return sorted(trades, reverse=True)[:k]          # O(n log n), totally acceptable
```
If pushed for "huge n, small k": keep a **min-heap of size k**. Each new value is compared to
the smallest of the current top k; if it's bigger, it replaces it. O(n log k).
```python
import heapq

def top_k_heap(trades, k):
    heap = []                                        # min-heap: heap[0] is the smallest
    for x in trades:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)               # pop smallest, push x
    return sorted(heap, reverse=True)
```
If you forget the `heapq` names, **describing the idea is enough**. If you want zero library
calls: keep a sorted list of length ≤ k and insert each new value in place (like insertion
sort), dropping the smallest when it grows past k. That's O(n·k), which is fine for small k.

### Part 4: streaming
- **State:** a min-heap (or small sorted list) of the current top k.
- **On each new trade:** if fewer than k stored, add it. Else if it beats the smallest stored,
  replace the smallest. Else ignore it. O(log k) per trade.
- **On a query:** return the stored k values sorted. O(k log k).
- **Contrast:** re-sorting all trades on every query would be O(n log n) each time and keeps
  growing all day. The heap only ever holds k items.
- **Good extra to raise:** "Does the window reset daily? Do trades ever get cancelled or
  corrected?" A busted trade would need to be **removed** from the top k, which a simple
  heap can't do cheaply. You'd need to keep more than k, or rebuild.

### Twist: long and short
Ask: **"Largest signed value, or largest by size?"** Argue for size: a 250-share short is a
bigger trade than a 100-share long. But confirm. For size, compare `abs(x)` and **return the
original signed value** (you rank by size but report reality):
```python
def top_three_by_size(trades):                       # trades: [(symbol, signed_qty), ...]
    best = []
    for t in trades:
        best.append(t)
        i = len(best) - 1
        while i > 0 and abs(best[i][1]) > abs(best[i - 1][1]):
            best[i], best[i - 1] = best[i - 1], best[i]
            i -= 1
        if len(best) > 3:
            best.pop()                               # drop the smallest
    return best
```
`[("AAPL",100),("MSFT",-250),("GOOG",50),("TSLA",-10),("NVDA",200)]` →
`[("MSFT",-250), ("NVDA",200), ("AAPL",100)]`.

Good questions to raise: rank by **quantity** or by **notional** (qty × price)? A 100-share
trade of a $1,000 stock is bigger than 1,000 shares of a $1 stock.
