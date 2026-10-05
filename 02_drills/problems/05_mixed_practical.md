# Drill Set 5 — Mixed Practical Problems

These are closer in spirit to the real interview: a short word problem, no hint about which
data structure to use. Read the whole prompt, decide your approach, *then* code.

## 1. Top three trade sizes
Given a list of trade sizes (ints), return the three largest, in descending order. If there
are fewer than three trades, return as many as there are, still sorted descending.
```
top_three([40, 10, 90, 30, 90, 5]) -> [90, 90, 40]
top_three([5, 1])                  -> [5, 1]
top_three([])                      -> []
```

## 2. Largest total by symbol
Given a list of `(symbol, quantity)` tuples representing trades, return the symbol with the
largest **total** quantity traded (summed across all its trades). Assume no ties.
```
largest_total([("AAPL", 100), ("GOOG", 50), ("AAPL", 80)]) -> "AAPL"   # AAPL total = 180
```

## 3. Parse and total a trade log
You're given a multi-line string, one trade per line, formatted `"SYMBOL,PRICE,QUANTITY"`.
Write `total_value(log)` that returns the total dollar value of all trades (`price * quantity`,
summed).
```python
log = """AAPL,150.0,10
GOOG,2800.0,2
AAPL,151.5,5"""
total_value(log) -> 7857.5     # 150*10 + 2800*2 + 151.5*5
```

## 4. Running maximum
Given a list of numbers, return a new list where each position holds the maximum value seen
so far (including the current position).
```
running_max([3, 1, 4, 1, 5, 9, 2]) -> [3, 3, 4, 4, 5, 9, 9]
```

## 5. Matching buy/sell orders
You have two lists of equal length: `buys` and `sells`, where `buys[i]` and `sells[i]` are
the price a trader is willing to buy/sell the `i`th unit at. A trade executes at position `i`
if `buys[i] >= sells[i]`. Write `count_matches(buys, sells)` returning how many positions
would execute.
```
count_matches([10, 5, 8], [9, 6, 8]) -> 2    # positions 0 and 2 match
```

## 6. Generalize: top k
Extend problem 1 to a general `top_k(nums, k)`. Don't sort the *entire* list if you can avoid
it when `k` is small relative to `len(nums)` — but a fully correct `sorted(nums, reverse=True)[:k]`
is a perfectly good first answer; only optimize further if asked.
```
top_k([40, 10, 90, 30, 90, 5], 2) -> [90, 90]
top_k([7], 5) -> [7]
```
Follow-up to think through (no code needed, just be ready to answer out loud): what would
you do differently if trades arrived **one at a time** (a stream) instead of as a full list
up front, and you needed to always be able to report the current top k?
