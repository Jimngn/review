# Answer Key — Mock 7 (Trade Log Parsing)

## Part 1 — clean parse
```python
def parse(lines):
    trades = []
    for line in lines:
        symbol, side, qty, price = line.split(",")
        trades.append({"symbol": symbol, "side": side,
                       "qty": int(qty), "price": float(price)})
    return trades
```
Narrate the type decisions: **`int` for quantity** (you can't trade 2.5 shares of most
things, and integer arithmetic is exact), **`float` for price** — and immediately add the
caveat you already know from the order book mock: *"if these were going into a matching
engine or an accounting system I'd use integer cents instead, but for aggregate reporting
float is fine."* Making that distinction unprompted is a strong signal.

Tuple vs dict vs class: a dict is self-documenting and the right default here; a
`namedtuple`/`dataclass` is better if this is going into a larger system. Say which and why
in one sentence, then move on — don't burn three minutes on it.

---

## Part 2 — notional
```python
def total_notional(trades):
    return sum(t["qty"] * t["price"] for t in trades)

def notional_by_symbol(trades):
    out = {}
    for t in trades:
        out[t["symbol"]] = out.get(t["symbol"], 0) + t["qty"] * t["price"]
    return out
```
Verified on the clean data: total **65,305.00**; per symbol **AAPL 18,800.00, MSFT
19,005.00, GOOG 27,500.00**.

Worth raising: should a SELL count as positive notional? For "total value traded," yes —
volume is unsigned. For cash flow, no. **Ask which they mean** rather than assuming; it's a
one-line question that shows you noticed the two readings.

---

## Part 3 — the messy parse

This is the part that's actually being scored. The structure that earns points:

```python
def parse(lines):
    trades, errors = [], []
    for lineno, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue                                  # blank lines are not errors
        fields = [f.strip() for f in line.split(",")]
        if len(fields) != 4:
            errors.append((lineno, line, f"expected 4 fields, got {len(fields)}"))
            continue
        symbol, side, qty, price = fields
        side = side.upper()
        if side not in ("BUY", "SELL"):
            errors.append((lineno, line, f"bad side {side!r}"));  continue
        try:
            qty, price = int(qty), float(price)
        except ValueError as e:
            errors.append((lineno, line, f"bad number: {e}"));    continue
        if qty <= 0 or price <= 0:
            errors.append((lineno, line, "qty and price must be positive")); continue
        trades.append({"symbol": symbol, "side": side, "qty": qty, "price": price})
    return trades, errors
```

Line-by-line, what each bad row is testing and what to say:

| Line | Issue | The answer |
|---|---|---|
| `  MSFT , SELL , 50 , 380.10` | padding | `.strip()` each field, not just the line |
| *(blank)* | empty line | Skip silently — a blank line is formatting, not corrupt data |
| `GOOG,BUY,ten,2750.00` | non-numeric qty | `try/except ValueError` around the conversion. **Catch `ValueError` specifically**, never bare `except:` |
| `TSLA,BUY,100` | missing field | Check field count *before* unpacking — otherwise you get an unpacking `ValueError` that's hard to attribute |
| `AAPL,buy,50,149.50` | lowercase | `.upper()`. Normalize rather than reject — case is almost never meaningful |
| `NVDA,BUY,-25,500.00` | negative qty | Reject. A negative buy is an unsigned sell; silently accepting it corrupts every downstream total |
| duplicate `AAPL,SELL,25,151.00` | ambiguous | **See below — do not silently dedupe** |

**The error-handling question is the real one.** Say this: *"I'll collect bad lines with
their line numbers and return them alongside the good records, rather than crashing or
dropping them. In a trading context a silently dropped trade is a position you don't know
you have — that's worse than a loud failure. Returning both lets the caller decide whether
to halt."* That reasoning is the answer; the `try/except` is just mechanics.

**The duplicate line.** There is no way to tell from this data whether it's a double-entry
bug or a genuine second trade of the same size at the same price — which happens constantly
in real markets. The correct response is to **say exactly that** and name what would settle
it: a trade ID, a timestamp, or a sequence number. Candidates who silently call `set()` on
the records have just deleted a real trade. Candidates who ask get the point.

---

## Part 4 — grouping and VWAP
```python
def summary(trades):
    out = {}
    for t in trades:
        s = out.setdefault(t["symbol"], {"bought": 0, "sold": 0, "notional": 0.0, "qty": 0})
        if t["side"] == "BUY":
            s["bought"] += t["qty"]
        else:
            s["sold"]   += t["qty"]
        s["notional"] += t["qty"] * t["price"]
        s["qty"]      += t["qty"]
    for s in out.values():
        s["net"]  = s["bought"] - s["sold"]
        s["vwap"] = s["notional"] / s["qty"] if s["qty"] else None
    return out
```
Verified on the clean data: **AAPL VWAP = 18,800 / 125 = 150.40**.

Points to make out loud:
- **Accumulate `notional` and `qty` in the same pass** rather than storing every trade and
  recomputing — one pass, O(1) state per symbol.
- **Guard the division**: a symbol with zero quantity would raise `ZeroDivisionError`. Say
  "VWAP of nothing is undefined, so `None`" — don't return 0, which reads as a real price.
- VWAP must use **total quantity, not the number of trades** — averaging the price column
  is a different (and usually wrong) number. If they ask "what's the difference?", that's
  the question: a 10,000-share trade should move the average more than a 1-share trade.

---

## Part 5 — complexity and scale
- **Parse is O(n)** in lines, O(1) work per line; grouping is O(n) with O(number of symbols)
  space.
- **50 GB file**: switch from a list to a **generator** — `for line in open(path)` streams
  and never holds the file in memory. Then say which operations survive: *sums, counts,
  min/max, VWAP accumulators all work streaming, because each is O(1) state updated per
  record. Anything needing the whole set at once — a median, exact distinct counts, sorting —
  does not.* That distinction is the actual insight they're probing.
  ```python
  def parse_stream(path):
      with open(path) as f:
          for line in f:
              ...
              yield record          # `yield`, not `.append`
  ```
- **Most volume without sorting**: one pass tracking the running best — O(n) and O(1) extra,
  versus O(n log n) to sort. Same idea as Mock 1's `largest()`. For top 3, `heapq.nlargest`.
- **Out of order with timestamps**: nothing changes for sums (addition is commutative), but
  anything path-dependent — FIFO P&L, running position, high-water marks — **requires sorting
  by timestamp first.** Naming the commutative/path-dependent split is the sharp answer.
