# The 7 Patterns That Cover Almost Every TDOE Coding Question

Your past questions (top k, adding strings) and every reported question are built from these
7 patterns. Get each template so automatic that you can write it without thinking, and
spend your thinking on the problem.

All examples use this trade shape:
```python
trades = [
    {"id": 1, "trader": "A", "symbol": "AAPL", "side": "BUY",  "qty": 100, "price": 150.00},
    {"id": 2, "trader": "B", "symbol": "MSFT", "side": "SELL", "qty":  50, "price": 300.00},
    {"id": 3, "trader": "A", "symbol": "AAPL", "side": "SELL", "qty":  30, "price": 151.00},
]
```

---

## 1. Loop and track the best so far
```python
best = None
for t in trades:
    if best is None or t["qty"] > best["qty"]:
        best = t
```
Start with `None`, not 0. With 0, an all-negative list gives a wrong answer silently.

## 2. Count / sum into a dict
```python
volume = {}
for t in trades:
    if t["symbol"] not in volume:
        volume[t["symbol"]] = 0
    volume[t["symbol"]] += t["qty"]
# shorter, same thing:  volume[s] = volume.get(s, 0) + t["qty"]
```

## 3. Group into a dict of lists
```python
by_trader = {}
for t in trades:
    if t["trader"] not in by_trader:
        by_trader[t["trader"]] = []
    by_trader[t["trader"]].append(t)
```

## 4. Sort by a field
```python
by_size = sorted(trades, key=lambda t: t["qty"], reverse=True)   # new list
trades.sort(key=lambda t: (t["symbol"], t["id"]))                # in place, two keys
```
Sorting is O(n log n). Mention it when you use it.

## 5. Parse a line of text
```python
line = " 1,A,AAPL,BUY,100,150.00 \n"
parts = line.strip().split(",")
if len(parts) != 6:
    pass                                  # bad line: skip or record an error
trade = {"id": int(parts[0]), "trader": parts[1], "symbol": parts[2],
         "side": parts[3], "qty": int(parts[4]), "price": float(parts[5])}
```
`int("abc")` raises a `ValueError`. If the data might be dirty, check first with
`parts[4].isdigit()` or wrap the conversion in `try/except ValueError`.

## 6. Walk from the end with a carry (digit-by-digit / two pointers)
```python
i, j = len(a) - 1, len(b) - 1
while i >= 0 or j >= 0:
    # use a[i] if i >= 0 else 0, same for b; then i -= 1, j -= 1
    ...
```
This is the add/subtract-strings pattern. It's also how you merge two sorted lists (two
pointers walking forward).

## 7. Validate: check every rule, collect errors, don't crash
```python
errors = []
for t in trades:
    if t["side"] not in ("BUY", "SELL"):
        errors.append((t["id"], "bad side"))
    if t["qty"] <= 0:
        errors.append((t["id"], "qty must be positive"))
```
For TDOE this matters a lot: **bad data should be reported, not silently dropped and not
allowed to crash the whole job.**

---

## Signed quantity: the one trading trick to know
```python
signed = t["qty"] if t["side"] == "BUY" else -t["qty"]
position[key] = position.get(key, 0) + signed
```
Buy = +, sell = −. Position = sum of signed quantities. Long if > 0, short if < 0, flat if 0.

---

## No-run gotchas (you can't execute code, so watch for these)

| Gotcha | Example | Fix |
|---|---|---|
| KeyError on a new dict key | `d[k] += 1` when `k` is new | `d.get(k, 0) + 1` or check `if k not in d` |
| Off-by-one in ranges | `range(1, n)` skips `n` | `range(n)` = 0..n−1 |
| Deleting from a list while looping over it | `for x in lst: lst.remove(x)` | Build a new list, or loop over a copy |
| Forgetting to `return` | function prints but returns `None` | Make sure every path returns |
| `sort()` returns `None` | `x = lst.sort()` | `x = sorted(lst)` |
| Integer vs float division | `7 / 2 = 3.5`, `7 // 2 = 3` | Pick the one you mean |
| Float equality on prices | `0.1 + 0.2 == 0.3` is **False** | Integer cents, or compare with a tolerance |
| Divide by zero | VWAP with no trades | Check for empty first |
| Swap order bug | `a = b; b = a` | `a, b = b, a` |
| String vs int | `"100" > "99"` is **False** (compares text) | Convert with `int()` first |

---

## How to "test" without running it
1. Pick the **smallest example** that exercises the logic (2–3 trades).
2. Make a little table of variable values per loop iteration.
3. Then run the edge cases in your head: **empty list, one item, ties, all the same key,
   bad value.**
4. Say "I'd also add a test for X" even if you don't write it. Interviewers notice this.
