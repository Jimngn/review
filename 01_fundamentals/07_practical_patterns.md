# Practical Patterns — turning a word problem into code

This is the glue file. Individually, variables/strings/lists/dicts/loops/functions are easy.
The actual skill being tested is: given a paragraph describing a process, pick the right
combination of these tools and wire them together correctly. These are the recurring shapes.

## 1. Parsing raw input into usable data
Real input is almost always text you must split and convert.
```python
line = "AAPL,150.25,100"
parts = line.split(",")                       # ["AAPL", "150.25", "100"]
ticker, price, qty = parts[0], float(parts[1]), int(parts[2])

# same thing, unpacked directly:
ticker, price_str, qty_str = line.split(",")
price, qty = float(price_str), int(qty_str)
```
If given multiple lines (e.g. from a file or multi-line string):
```python
raw = """AAPL,150.25,100
GOOG,2800.00,10"""

rows = []
for line in raw.strip().split("\n"):
    ticker, price, qty = line.split(",")
    rows.append((ticker, float(price), int(qty)))
```
Watch for: trailing whitespace/newlines (`.strip()` first), inconsistent delimiters, and
whether numeric fields should be `int` or `float`.

## 2. Counting / frequency
Whenever a problem says "how many times", "most common", "find duplicates" — dict or Counter.
```python
counts = {}
for item in items:
    counts[item] = counts.get(item, 0) + 1

most_common_item = max(counts, key=counts.get)   # key with the highest count
```
`max(iterable, key=fn)` — `key` tells `max` what to compare *by*, without changing what gets
returned. This is a genuinely high-value idiom; the same trick works with `min` and `sorted`.

## 3. Sorting by something other than natural order
```python
people = [("Nick", 30), ("Amy", 25), ("Ben", 40)]

sorted(people, key=lambda p: p[1])              # sort by age (2nd element)
sorted(people, key=lambda p: p[1], reverse=True) # oldest first
```
`lambda p: p[1]` is a tiny anonymous function meaning "given p, return p[1]". Read it as
shorthand for `def get_age(p): return p[1]`, then `sorted(people, key=get_age)` — write it
that longer way first if lambda syntax feels shaky, then compress it once it's second nature.

## 4. Deduplicating while preserving order
`set()` dedupes but loses order. When order matters:
```python
seen = set()
result = []
for x in items:
    if x not in seen:
        seen.add(x)
        result.append(x)
```

## 5. Two lists that correspond to each other
```python
names = ["Nick", "Amy"]
scores = [90, 85]
for name, score in zip(names, scores):
    print(name, score)
```

## 6. Running/simulating a process over time (state machine in a loop)
A lot of "practical" problems (process these transactions in order, track a running balance,
simulate an inventory) have this shape: some state variables, updated inside a loop, one
event/line at a time.
```python
balance = 0
for amount in transactions:
    balance += amount
    if balance < 0:
        print("overdrawn!")
```
The habit to build: identify *what state needs to persist across iterations* (here,
`balance`) before writing the loop, initialize it correctly (often 0, `[]`, `{}`, or `None`),
then figure out the one update rule applied each iteration.

## 7. Building a lookup table, then using it
Two-pass pattern: first pass builds a dict, second pass uses it.
```python
# price lookup by ticker
prices = {}
for ticker, price in price_rows:
    prices[ticker] = price

# now answer queries in O(1) instead of re-scanning price_rows each time
for ticker in queries:
    print(prices.get(ticker, "unknown"))
```

## 8. Filtering
```python
positives = [x for x in nums if x > 0]
# equivalent explicit loop, if comprehension syntax is shaky:
positives = []
for x in nums:
    if x > 0:
        positives.append(x)
```

## Edge-case checklist — run through this before saying "done"
- **Empty input**: empty list/string/dict. Does your loop just do nothing gracefully, or
  does `nums[0]` / `max([])` crash?
- **Single element**: does your logic that assumes "compare to the previous element" break
  on the first element (no previous element yet)?
- **Duplicates**: if using `.index()` or `.remove()`, remember they act on the *first* match
  only.
- **Off-by-one**: slice/range bounds are inclusive-start, exclusive-stop — always sanity
  check with a tiny example (`range(0,3)` → 0,1,2, not 0,1,2,3).
- **Integer vs float division**: `/` always gives float; use `//` if you need an int.
- **Case sensitivity**: `"Apple" == "apple"` is `False` — `.lower()` both sides if the
  problem implies case-insensitive comparison.
- **Mutating the thing you're iterating over**: modifying a list while looping over it
  (e.g. `.remove()` inside a `for x in mylist` loop) skips elements — build a new list or
  iterate over a copy (`for x in mylist[:]`) instead.
