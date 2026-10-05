# Answers: Trade Data Analysis

All code here was run against tests (including the edge cases mentioned). It's written
plainly on purpose: this is the style to aim for when you can't run your code.

---

## 1. Parse a trade file
**Clarify first:** "Is there a header line? Can there be extra spaces? What should happen with a
bad line: skip it, or stop?"

```python
def parse_trades(lines):
    trades = []
    for line in lines:
        parts = line.strip().split(",")
        trades.append({
            "id": int(parts[0]),
            "trader": parts[1],
            "symbol": parts[2],
            "side": parts[3],
            "qty": int(parts[4]),
            "price": float(parts[5]),
        })
    return trades
```

**Follow-up: don't crash on bad lines.**
```python
def parse_trades_safe(lines):
    trades = []
    errors = []
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "":
            errors.append((line_num, "empty line"))
            continue
        parts = line.split(",")
        if len(parts) != 6:
            errors.append((line_num, "expected 6 fields, got " + str(len(parts))))
            continue
        try:
            trade = {
                "id": int(parts[0]),
                "trader": parts[1],
                "symbol": parts[2],
                "side": parts[3],
                "qty": int(parts[4]),
                "price": float(parts[5]),
            }
        except ValueError:
            errors.append((line_num, "bad number"))
            continue
        trades.append(trade)
    return trades, errors
```
Say: "I return the errors instead of printing them, so the caller can decide what to do.
Silently dropping bad trades is dangerous: a missing trade means a wrong position."

---

## 2. Volume per symbol
```python
def volume_by_symbol(trades):
    volume = {}
    for t in trades:
        volume[t["symbol"]] = volume.get(t["symbol"], 0) + t["qty"]
    return volume
```
**A: most traded.** Ask about ties. Here, return all the tied symbols:
```python
def most_traded(trades):
    volume = volume_by_symbol(trades)
    best = None
    for qty in volume.values():
        if best is None or qty > best:
            best = qty
    winners = []
    for symbol, qty in volume.items():
        if qty == best:
            winners.append(symbol)
    return winners                      # [] if there were no trades
```
**B: sorted by volume:** `sorted(volume.items(), key=lambda kv: kv[1], reverse=True)`
gives a list of `(symbol, qty)` pairs. O(n) to build the dict, O(s log s) to sort the s symbols.

---

## 3. Net position per trader
```python
def positions(trades):
    pos = {}
    for t in trades:
        key = (t["trader"], t["symbol"])
        if t["side"] == "BUY":
            signed = t["qty"]
        else:
            signed = -t["qty"]
        pos[key] = pos.get(key, 0) + signed
    return pos
```
**A: fully flat traders.** A trader is flat only if **every** symbol they traded nets to 0:
```python
def flat_traders(trades):
    pos = positions(trades)
    not_flat = set()
    all_traders = set()
    for (trader, symbol), qty in pos.items():
        all_traders.add(trader)
        if qty != 0:
            not_flat.add(trader)
    return all_traders - not_flat
```
**B: tuple key vs nested dict:** a tuple key is simpler to update (one line, no
"does the inner dict exist?" check). A nested dict `{trader: {symbol: qty}}` makes "show me
everything for trader A" easy. Pick based on the question you'll be asked most.

---

## 4. VWAP per symbol
```python
def vwap_by_symbol(trades):
    qty_sum = {}
    notional_sum = {}
    for t in trades:
        s = t["symbol"]
        qty_sum[s] = qty_sum.get(s, 0) + t["qty"]
        notional_sum[s] = notional_sum.get(s, 0) + t["qty"] * t["price"]
    result = {}
    for s in qty_sum:
        if qty_sum[s] > 0:
            result[s] = notional_sum[s] / qty_sum[s]
    return result
```
**Why not average prices:** 1 share @ $100 and 999 shares @ $10. Plain average = $55. VWAP =
(100 + 9,990) / 1,000 = **$10.09**. Almost everything actually traded around $10. VWAP
reflects what was really paid.

---

## 5. Validate trades
```python
def validate(trades, allowed_symbols):
    errors = []
    seen_ids = set()
    for t in trades:
        tid = t["id"]
        if tid in seen_ids:
            errors.append((tid, "duplicate id"))
        seen_ids.add(tid)
        if t["side"] != "BUY" and t["side"] != "SELL":
            errors.append((tid, "bad side"))
        if not isinstance(t["qty"], int) or t["qty"] <= 0:
            errors.append((tid, "qty must be a positive integer"))
        if t["price"] <= 0:
            errors.append((tid, "price must be positive"))
        if t["symbol"] not in allowed_symbols:
            errors.append((tid, "unknown symbol"))
    return errors
```
- Use a **set** for `seen_ids`: O(1) lookups, so the whole thing is O(n).
- Use separate `if`s, not `elif`, so one trade can report several problems.
- If fields might be **missing**, ask, then use `t.get("qty")` and add a "missing field" check
  before the others.

**Follow-up (10x price):** that's a **warning**, not an error. The trade really happened; a
fat finger or a bad price feed is still a fact you have to book. Compute the average price
per symbol first (one pass), then flag trades where `price > 10 * avg` or `price < avg / 10`
into a separate `warnings` list for a human to check. TDOE instinct: **flag and escalate,
don't silently "fix" or drop.**

---

## 6. Top of book from a snapshot
```python
def top_of_book(orders):
    best_bid = None
    best_ask = None
    for o in orders:
        if o["side"] == "BUY":
            if best_bid is None or o["price"] > best_bid:
                best_bid = o["price"]
        else:
            if best_ask is None or o["price"] < best_ask:
                best_ask = o["price"]
    return best_bid, best_ask
```
**A: size at the top.** After finding the best prices, do a second pass that sums `qty` for
orders at exactly those prices. Two passes is still O(n), and clearer than one clever pass.
```python
def top_of_book_with_size(orders):
    best_bid, best_ask = top_of_book(orders)
    bid_size = 0
    ask_size = 0
    for o in orders:
        if o["side"] == "BUY" and o["price"] == best_bid:
            bid_size += o["qty"]
        if o["side"] == "SELL" and o["price"] == best_ask:
            ask_size += o["qty"]
    return best_bid, bid_size, best_ask, ask_size
```
**B: crossed.**
```python
def is_crossed(orders):
    best_bid, best_ask = top_of_book(orders)
    if best_bid is None or best_ask is None:
        return False
    return best_bid >= best_ask
```
Note `>=`: equal prices would have traded, so a book with bid == ask is also invalid.
**What it tells you:** the exchange's matching engine never leaves a crossed book, so **our
copy is wrong**. We probably missed a message (a fill or cancel), processed messages out
of order, or are combining data from two sources that are out of sync. Investigate the feed,
not the market.

---

## 7. Reconcile
```python
def reconcile(ours, theirs):
    ours_by_id = {}
    for t in ours:
        ours_by_id[t["id"]] = t
    theirs_by_id = {}
    for t in theirs:
        theirs_by_id[t["id"]] = t

    missing_from_ours = []
    missing_from_theirs = []
    mismatched = []
    for tid in theirs_by_id:
        if tid not in ours_by_id:
            missing_from_ours.append(tid)
    for tid in ours_by_id:
        if tid not in theirs_by_id:
            missing_from_theirs.append(tid)
        else:
            a = ours_by_id[tid]
            b = theirs_by_id[tid]
            if a["qty"] != b["qty"] or a["price"] != b["price"] or a["side"] != b["side"]:
                mismatched.append(tid)
    return missing_from_ours, missing_from_theirs, mismatched
```
**Complexity:** nested loops = O(n × m). Building a dict by ID first makes every lookup
O(1), so the total is **O(n + m)**. This is the most useful idea in all of TDOE coding:
"**turn one list into a dict keyed by ID, then loop over the other.**"

Also say: "If our list has the same ID twice, the dict would silently keep only the last one.
I'd check for duplicates first." That's a great thing to raise unprompted.

---

## 8. Position limit breach
```python
def first_breach(trades, limit):
    pos = {}
    for t in trades:
        key = (t["trader"], t["symbol"])
        if t["side"] == "BUY":
            signed = t["qty"]
        else:
            signed = -t["qty"]
        pos[key] = pos.get(key, 0) + signed
        if abs(pos[key]) > limit:
            return t["id"]
    return None
```
**Follow-up:** collect IDs in a list instead of returning. For −600 → −550: the position is
still over the limit, but the trade **reduces risk**. Most risk systems allow risk-reducing
trades (you *want* the trader to get back under), so a sensible rule is "breach if
`abs(new) > limit` **and** `abs(new) > abs(old)`". The point is to **ask** which the business
wants rather than guess.

---

## 9. O(n) sort for a short array (counting sort)
```python
def counting_sort(sizes, max_value):
    counts = [0] * (max_value + 1)          # counts[v] = how many times v appears
    for s in sizes:
        counts[s] += 1
    result = []
    for value in range(max_value + 1):
        for _ in range(counts[value]):
            result.append(value)
    return result
```
`counting_sort([3, 1, 10, 3, 7, 1, 1], 10)` → `[1, 1, 1, 3, 3, 7, 10]`.

- **Why O(n):** no comparisons. One pass to count (n) plus one pass over the possible
  values (k = 10). Total O(n + k), which is O(n) when k is small and fixed.
- **Bad idea when:** the range is huge (sizes up to 1,000,000 means a million-slot list for
  7 numbers), or values aren't small integers (prices like 15.37, strings).

**"Only 5 elements": insertion sort.** Simple, no extra memory, and for tiny n the
O(n²) doesn't matter:
```python
def insertion_sort(a):
    a = list(a)                             # don't change the caller's list
    for i in range(1, len(a)):
        current = a[i]
        j = i - 1
        while j >= 0 and a[j] > current:
            a[j + 1] = a[j]                 # shift bigger items right
            j -= 1
        a[j + 1] = current
    return a
```

---

## 10. Merge two time-sorted streams
```python
def merge(a, b):
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i]["time"] <= b[j]["time"]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    while i < len(a):                       # one list ran out, so copy the rest of the other
        result.append(a[i])
        i += 1
    while j < len(b):
        result.append(b[j])
        j += 1
    return result
```
- O(n + m). `<=` keeps the merge **stable** (ties go to `a` first). Say what you chose for ties.
- The bug people make: forgetting the two "copy the rest" loops.

**k exchanges (verbal):** keep a **min-heap** of the next trade from each stream: pop the
smallest, then push the next trade from that same stream. O(N log k). Simpler fallback: merge
them two at a time.
