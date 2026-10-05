# Mock 8 — Positions and P&L (dict aggregation, ~45 min)

"Grouping and summing with dictionaries" in the framing Jane Street actually uses. This mock
escalates from counting into real trading logic — the later parts are where the interesting
reasoning is, and where most candidates discover their Part 1 data structure was wrong.

45-minute timer. No reading ahead.

---

## Working data
```python
trades = [
    ("AAPL", "BUY",  100, 150.00),
    ("AAPL", "BUY",  100, 152.00),
    ("MSFT", "BUY",   50, 380.00),
    ("AAPL", "SELL", 150, 155.00),
    ("MSFT", "SELL",  50, 375.00),
    ("GOOG", "BUY",   10, 2750.00),
]
```

## Part 1 — net position per symbol (5 min)
`positions(trades)` → `{"AAPL": 50, "MSFT": 0, "GOOG": 10}`

Buys add, sells subtract. Say out loud why a `defaultdict(int)` or `dict.get(k, 0)` is
cleaner than checking membership every time — and be ready for *"what if I don't want the
`collections` import?"*

Follow-up: should a symbol that nets to zero still appear in the output? Argue a position.

---

## Part 2 — cash flow and realized P&L (15 min)
> "How much money did we spend and receive?"

Buys are cash out, sells are cash in. Then the real question:
> "What's our profit on AAPL?"

This is where it gets interesting, and you should surface the ambiguity yourself: we bought
100 @ 150 and 100 @ 152, then sold 150 @ 155. **Which shares did we sell?**
- **FIFO** — the 100 @ 150 first, then 50 of the 152s.
- **Average cost** — all shares cost 151.00.
- **LIFO** — the 152s first.

Pick one, say why, and compute it. Then state what the *other* convention would have given.
Naming the ambiguity before being asked is the single highest-scoring moment in this mock —
it's exactly the kind of "there's a business decision hiding in this code" judgment the role
is testing for.

---

## Part 3 — unrealized P&L and marking to market (10 min)
> "Here are the current prices. What's our P&L now?"
```python
marks = {"AAPL": 157.00, "MSFT": 378.00, "GOOG": 2800.00}
```
Total P&L = realized (from closed trades) + unrealized (open position marked at current
price). Compute both separately and explain the difference out loud — unrealized P&L is
money you'd have *if* you sold now, and it moves every second without you trading.

Edge cases to raise yourself: a symbol with no mark available; a **short** position (negative
quantity — does your formula still work?); a position of exactly zero.

---

## Part 4 — top movers (10 min)
> "Which three symbols have the largest absolute P&L?"

Note out loud this is Mock 1's top-k again, now over dictionary values with a key function
and an absolute value. Be precise about **absolute** — a $1M loss is a bigger mover than a
$10k gain, so the biggest loser must rank.

Follow-up: *"What if there are 10,000 symbols and you only want the top 3?"*

---

## Part 5 — the structure question (5 min)
> "Suppose trades stream in all day and I need the current position at any moment."

Verbal only. What's your state, what does each incoming trade update, and what's the cost
per trade? Contrast it with recomputing from the full trade list every time, and give the
complexity of each.

Final one to be ready for: *"Two threads are updating positions for the same symbol."* You
aren't expected to write locking code — just recognize the hazard out loud.
