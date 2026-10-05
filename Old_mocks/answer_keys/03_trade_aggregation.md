# Answer Key — Mock 3 (Trade Aggregation)

## Part 1 — total quantity per symbol
```python
def total_quantity_by_symbol(trades):
    totals = {}
    for symbol, price, qty in trades:
        totals[symbol] = totals.get(symbol, 0) + qty
    return totals
```
Direct application of the dict-accumulator/counting pattern, just keyed by `symbol` and
summing `qty` instead of counting occurrences. Unpacking `symbol, price, qty` directly in
the `for` line (rather than indexing `trade[0]`, `trade[1]`, `trade[2]`) is both cleaner and
less error-prone — prefer it whenever the tuple shape is known and fixed.

## Part 2 — symbol with highest total value
```python
def symbol_with_highest_value(trades):
    totals = {}
    for symbol, price, qty in trades:
        totals[symbol] = totals.get(symbol, 0) + price * qty
    return max(totals, key=totals.get)
```
Same accumulator shape, just accumulating `price * qty` instead of `qty` alone. Then the
now-familiar `max(dict, key=dict.get)` idiom picks out the top key.

## Part 3 — filtering erroneous trades
```python
def total_quantity_by_symbol(trades):
    totals = {}
    for symbol, price, qty in trades:
        if qty <= 0:
            continue
        totals[symbol] = totals.get(symbol, 0) + qty
    return totals
```
The filter belongs **inside the loop, before the accumulation line** — `continue` skips
straight to the next trade without touching `totals` at all for a bad record. Putting the
filter in a separate pass first (`trades = [t for t in trades if t[2] > 0]`, then loop) is
equally correct and arguably clearer to read — either is fine to say out loud as an
alternative; picking one and being able to justify it is what matters.

## Part 4 — manual trace
`trades = [("AAPL", 100.0, 3), ("GOOG", 50.0, 10), ("AAPL", 100.0, 4)]`, computing value
totals:

| trade processed | value added | totals after |
|---|---|---|
| ("AAPL", 100.0, 3) | 100.0 * 3 = 300.0 | {"AAPL": 300.0} |
| ("GOOG", 50.0, 10) | 50.0 * 10 = 500.0 | {"AAPL": 300.0, "GOOG": 500.0} |
| ("AAPL", 100.0, 4) | 100.0 * 4 = 400.0 | {"AAPL": 700.0, "GOOG": 500.0} |

`max(totals, key=totals.get)` then compares 700.0 vs 500.0 and returns `"AAPL"`.

## Part 5 — adapting to raw text input
```python
def symbol_with_highest_value(raw):
    totals = {}
    for line in raw.strip().split("\n"):
        symbol, price, qty = line.split(",")
        price, qty = float(price), int(qty)
        totals[symbol] = totals.get(symbol, 0) + price * qty
    return max(totals, key=totals.get)
```
**What changes:** you need a parsing step up front — `.strip().split("\n")` to get lines,
then `line.split(",")` to get the three string fields, then explicit `float()`/`int()`
conversion, since everything from `.split()` is a string. **What stays exactly the same:**
the accumulation logic (`totals.get(symbol, 0) + price * qty`) and the final `max(...)` call
— the aggregation logic doesn't care how the data arrived, only that by the time it reaches
that line, `symbol` is a string and `price`/`qty` are numbers. This separation (parse once at
the boundary, then work with clean typed data) is worth stating explicitly — it's a good
instinct to demonstrate, not just a coincidence of this example.
