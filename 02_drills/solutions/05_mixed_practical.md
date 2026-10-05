# Solutions — Drill Set 5 (Mixed Practical)

## 1. Top three trade sizes
```python
def top_three(trades):
    return sorted(trades, reverse=True)[:3]
```
Sort descending, take the first 3 — slicing past the end of a list (`[:3]` on a 2-element
list) doesn't error, it just returns what's there, which conveniently handles the
"fewer than three" and "empty list" cases for free. Worth saying out loud: this is O(n log n)
because of the sort; see problem 6 for the O(n) alternative when only a few "top" values are
needed out of a much larger list.

## 2. Largest total by symbol
```python
def largest_total(trades):
    totals = {}
    for symbol, qty in trades:
        totals[symbol] = totals.get(symbol, 0) + qty
    return max(totals, key=totals.get)
```
Build a running total per symbol (the dict-accumulator pattern), then `max(dict, key=dict.get)`
picks the key with the largest value — same idiom as "most common element" in drill set 3.

## 3. Parse and total a trade log
```python
def total_value(log):
    total = 0
    for line in log.strip().split("\n"):
        symbol, price, qty = line.split(",")
        total += float(price) * int(qty)
    return total
```
`.strip()` first removes any stray leading/trailing whitespace/newlines so `.split("\n")`
doesn't produce an empty trailing line. Each line is comma-split into three string fields;
`price` becomes a `float`, `qty` an `int`, and only their *product* is accumulated — the
`symbol` field is unpacked but unused here, which is fine, it's still required to unpack
correctly.

## 4. Running maximum
```python
def running_max(nums):
    result = []
    current_max = nums[0]
    for x in nums:
        current_max = max(current_max, x)
        result.append(current_max)
    return result
```
Same accumulator shape as running total, but with `max()` as the update rule instead of `+`.
**Edge case to flag out loud**: this assumes `nums` is non-empty (`nums[0]` would crash on
`[]`) — if empty input is possible, check for it first and return `[]`.

## 5. Matching buy/sell orders
```python
def count_matches(buys, sells):
    count = 0
    for buy, sell in zip(buys, sells):
        if buy >= sell:
            count += 1
    return count
```
`zip` pairs up corresponding elements from the two lists so you never have to index by `i`
manually — a direct application of the "two lists that correspond to each other" pattern.

## 6. Generalize: top k
```python
def top_k(nums, k):
    return sorted(nums, reverse=True)[:k]
```
The straightforward, always-correct answer — same as problem 1 but parameterized. It's
O(n log n) because of the full sort. If asked "can you avoid sorting everything when `k` is
small": the idea is to keep only a small running collection of the best `k` values seen so
far as you scan once through `nums` (conceptually a "top-k tracker"; Python's
`heapq.nlargest(k, nums)` does exactly this in one line, or `heapq` more generally, if you
remember the import) — getting this to O(n log k) instead of O(n log n). Saying this
trade-off out loud, even without writing the heap version live, is a strong answer.

**Streaming follow-up** (talk-through, not code): if trades arrive one at a time rather than
as a full list, you can't re-sort from scratch on every new value — you'd maintain a
small structure (e.g. a min-heap of size k) holding the current top k, and each new value
only needs to be compared against the *smallest* of those k to decide if it belongs, updating
in O(log k) per new trade instead of re-sorting everything.
