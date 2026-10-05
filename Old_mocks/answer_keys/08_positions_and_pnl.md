# Answer Key — Mock 8 (Positions and P&L)

All figures below are computed, not estimated — see the trace tables.

## Part 1 — net position
```python
from collections import defaultdict

def positions(trades):
    pos = defaultdict(int)
    for symbol, side, qty, price in trades:
        pos[symbol] += qty if side == "BUY" else -qty
    return dict(pos)
```
Verified: `{"AAPL": 50, "MSFT": 0, "GOOG": 10}`.

Without `collections`: `pos[symbol] = pos.get(symbol, 0) + delta`. Know both — the
`.get(k, 0)` form is the one to reach for when you're unsure the import is available, and
mentioning that you know both takes two seconds.

**Should MSFT (net 0) appear?** Argue it both ways and pick: *"I'd keep it, because 'we
traded MSFT today and are now flat' is different information from 'we never touched MSFT',
and a reconciliation report needs that distinction. If this fed an order router I'd filter
zeros out."* The judgment is the point, not the choice.

---

## Part 2 — cash flow and realized P&L
```python
def cash_flow(trades):
    cash = 0.0
    for symbol, side, qty, price in trades:
        cash += -qty * price if side == "BUY" else qty * price
    return cash
```
Verified: spent **76,700**, received **42,000**, net cash **-34,700**. Negative cash is
expected — we're still holding 50 AAPL and 10 GOOG that we paid for.

### The AAPL question — surface the ambiguity yourself
We bought 100 @ 150 and 100 @ 152, then sold 150 @ 155. **Which 150 shares did we sell?**
The data cannot answer that; it's an accounting convention.

| Convention | Realized P&L | Remaining 50 shares cost basis |
|---|---|---|
| **FIFO** (oldest first) | **650** | 152.00 |
| **Average cost** (all shares cost 151.00) | **600** | 151.00 |
| **LIFO** (newest first) | **550** | 150.00 |

FIFO worked out: sell 100 of the 150-lot → 100 x (155-150) = 500; then 50 of the 152-lot →
50 x (155-152) = 150. Total **650**, with 50 shares @ 152 left.

```python
from collections import deque, defaultdict

def realized_fifo(trades):
    lots = defaultdict(deque)       # symbol -> deque of [qty, cost] open lots
    realized = defaultdict(float)
    for symbol, side, qty, price in trades:
        if side == "BUY":
            lots[symbol].append([qty, price])
        else:
            remaining = qty
            while remaining > 0:
                lot_qty, lot_price = lots[symbol][0]
                take = min(remaining, lot_qty)
                realized[symbol] += take * (price - lot_price)
                remaining -= take
                if take == lot_qty:
                    lots[symbol].popleft()
                else:
                    lots[symbol][0][0] -= take
    return dict(realized), lots
```
Note the structure: a **FIFO queue of open lots per symbol** — the same price-time-priority
shape as the order book's queue at a price level. Point that out; connecting the two
problems is exactly the kind of transfer they're looking for.

Edge case to raise: selling more than you hold. The loop above would `IndexError` on an
empty deque. In reality that's a **short position** — say so, and say you'd either reject it
or open a negative lot depending on whether shorting is allowed.

---

## Part 3 — mark to market

```python
def pnl(trades, marks):
    realized, lots = realized_fifo(trades)
    out = {}
    for symbol in set(t[0] for t in trades):
        unrealized = sum(q * (marks[symbol] - cost) for q, cost in lots.get(symbol, []))
        out[symbol] = {"realized": realized.get(symbol, 0.0),
                       "unrealized": unrealized,
                       "total": realized.get(symbol, 0.0) + unrealized}
    return out
```
Verified at marks AAPL 157, MSFT 378, GOOG 2800:

| Symbol | Realized | Unrealized | Total |
|---|---|---|---|
| AAPL | 650 | 250 | **900** |
| MSFT | -250 | 0 | **-250** |
| GOOG | 0 | 500 | **500** |
| **Portfolio** | 400 | 750 | **1,150** |

### The insight to volunteer here
**The cost convention changes the realized/unrealized split, but not the total.** Verified:

| Convention | Realized | Unrealized | Total |
|---|---|---|---|
| FIFO | 650 | 250 | **900** |
| Average | 600 | 300 | **900** |
| LIFO | 550 | 350 | **900** |

Why: total P&L is just `proceeds - cost + position x mark` = `23,250 - 30,200 + 7,850 = 900`,
which never mentions lot matching. The convention only decides *when* profit is recognized,
not how much there is. **Saying this unprompted is the single best moment available in this
mock** — it shows you understand what the accounting is actually doing rather than just
implementing a rule. (It's also why the convention matters so much for tax and so little for
risk.)

Other edge cases to raise yourself:
- **Missing mark** — don't default to 0, which would report a total loss on a position you
  still hold. Return `None` or flag it.
- **Short position** — `qty x (mark - cost)` still works with negative quantity: if you're
  short 50 at 150 and the mark rises to 157, you get `-50 x 7 = -350`, correctly a loss.
  State that you checked the sign convention rather than assuming.
- **Zero position** — unrealized is 0; all the P&L is realized.

---

## Part 4 — top movers
```python
def top_movers(pnl_by_symbol, k=3):
    return sorted(pnl_by_symbol.items(),
                  key=lambda kv: abs(kv[1]["total"]), reverse=True)[:k]
```
Verified: **AAPL (900), GOOG (500), MSFT (-250)** — MSFT ranks third on magnitude 250
despite being a loss, which is the whole point of `abs`.

Say it out loud: *"'Largest' means largest magnitude — a big loss is a big mover. I'm
sorting on `abs` but reporting the signed value, because dropping the sign in the output
would be misleading."*

**10,000 symbols, top 3** — this is Mock 1 again, and you should name the link:
`heapq.nlargest(3, items, key=...)` is O(n log k) instead of O(n log n). With k=3 and
n=10,000 that's a real difference, and the mechanism is the min-heap of size k.

---

## Part 5 — streaming state
**Keep the aggregates, not the trades.** Per symbol: position, realized P&L, and the open
lot queue. Each incoming trade is **O(1)** (amortized — a sell may consume several lots, but
each lot is consumed once). Recomputing from the full history is **O(n) per query** and grows
without bound all day.

The trade-off to name: incremental state is fast but **path-dependent and unauditable** —
if a bad trade arrives you can't easily un-apply it. Many real systems keep the full
immutable trade log *and* an incremental cache, replaying from the log to recover. That
answer — "both, for different reasons" — is better than either alone.

**Two threads, same symbol**: the classic read-modify-write race. `pos[symbol] += qty` is
not atomic — two threads can both read 100, both write 150, and you've lost a trade.
Options: a lock per symbol; or a single-writer design where all updates for a symbol go
through one thread/queue, which is how most trading systems actually do it and avoids lock
contention entirely. **You are not expected to write this** — recognizing the hazard and
naming single-writer is the full-credit answer.
