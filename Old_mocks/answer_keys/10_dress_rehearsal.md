# Answer Key — Mock 10 (Dress Rehearsal)

## A1 — warm-up
A limit order with nothing on the other side **rests on the book**: it's added to the queue
at its price level and becomes a resting order, available for someone else to trade against.
No trade, no error. Good extra sentence: *"It's now providing liquidity rather than taking
it, and it sits there until it's filled, cancelled, or the session ends."*

---

## A3 — the hand trace (verified against the reference engine)

```
add A BUY 10.00 x100   -> no offers. A rests.
   BIDS: 10.00 [A:100]

add B BUY 10.00 x50    -> no offers. B rests BEHIND A (same price, later arrival).
   BIDS: 10.00 [A:100, B:50]

add C BUY  9.99 x200   -> rests at a new, worse level.
   BIDS: 10.00 [A:100, B:50] | 9.99 [C:200]

add D SELL 10.01 x75   -> best bid 10.00; sell crosses only if 10.01 <= 10.00. It does not.
   D rests.
   BIDS: 10.00 [A:100, B:50] | 9.99 [C:200]      ASKS: 10.01 [D:75]

cancel A               -> A removed. B is now at the front of the 10.00 queue.
   BIDS: 10.00 [B:50] | 9.99 [C:200]             ASKS: 10.01 [D:75]

add E SELL 10.00 x120
   pass 1: best bid 10.00; 10.00 <= 10.00 -> CROSS.
           front of level is B (A is gone).
           trade min(120, 50) = 50 @ $10.00  [buy B / sell E]
           B exhausted and removed. E has 70 left.
   pass 2: best bid is now 9.99. Does E cross? 10.00 <= 9.99 is FALSE. NO CROSS.
           Loop exits.
   E's remaining 70 RESTS as an offer at 10.00.
```

**Final state:**
```
ASK  $10.01   75     (D)
ASK  $10.00   70     (E, the unfilled remainder)
------------------
BID  $ 9.99  200     (C)
```
**Trades: exactly one — 50 @ $10.00, B buying from E.**

### The trap, spelled out
The prompt dangles "then 70 against C at $9.99." **That is wrong, and it's the whole point.**
E is a sell order with a **limit of 10.00** — it will not sell at 9.99, because a limit price
is a floor for a seller. A market order would have swept down to C; a limit order stops at
its limit and rests.

If you accepted that line without checking, the lesson is: **when an interviewer states an
expected result, verify it rather than agreeing.** They do this on purpose. Agreeing with a
confidently-stated wrong answer is one of the few things that reliably fails a candidate
here, and pushing back politely with your reasoning is one of the few things that reliably
impresses.

Two sub-points also worth saying out loud during the trace:
- Cancelling A **promotes B**, it doesn't reshuffle the level — B keeps the position it
  earned by arriving second, it just has nobody ahead of it now.
- E ends up resting at 10.00 **on the offer side**, while D rests at 10.01. The book is
  perfectly consistent: best ask is now 10.00, and the spread is 0.01 against C's 9.99.

---

## A2 — escalation notes (differences from Mock 5)

**4. "Replace — same ID, new price and new size."** This is `modify_price` and `modify_qty`
at once, and the answer is unambiguous: a replace that changes price **always goes to the
back of the queue**. Implement it as cancel-then-add so a replace that crosses trades
immediately. The thing to say: *"Same ID is a protocol convenience; priority-wise this is a
brand new order."*

**5. "Fill completely right now or not at all"** = fill-or-kill. The pre-check pass is the
answer — see Mock 6 key, Part 6. You cannot discover insufficient size halfway through,
because the earlier trades have already printed.

**6. Self-trade** — see Mock 6 key, Part 7. Name the three policies, pick one, mention wash
trading.

---

## B1 — quote feed (all figures verified)

**Latest quote per symbol**: AAPL `150.10 / 150.12` @ 09:30:05; MSFT `379.95 / 380.20`
@ 09:30:07. One pass, overwriting a dict — last write wins. Only valid because the feed is
in timestamp order; **say that assumption out loud**, because if it isn't, you need to compare
timestamps rather than overwrite.

**Average spread**: AAPL spreads are 0.05, 0.02, 0.02 → **0.03**. MSFT: 0.10, 0.25 → **0.175**.

> **The float trap, and it is real.** Computed raw, those spreads come out as
> `0.05000000000001137`, `0.10000000000002274`, `0.01999999999998181`. So
> `max()` still works, but any **equality** test (`spread == 0.02`), any grouping by spread,
> and any printed output is wrong or ugly. This is the same lesson as the order book, now
> biting in a different place — **round at the boundary, or work in integer cents.** Spotting
> this in a parsing problem, where candidates don't expect it, is a standout moment.

**Widest spread at any point**: **MSFT, 0.25, at 09:30:07.** One pass tracking the running
max — O(n), O(1) extra. Do not sort.

**Spread widened from the previous update**: **MSFT only** (0.10 → 0.25 at 09:30:07). AAPL
narrowed then stayed flat. This one needs **per-symbol previous-value state**:
```python
prev = {}
for symbol, bid, ask, ts in quotes:
    spread = round(ask - bid, 4)
    if symbol in prev and spread > prev[symbol]:
        widened.append((symbol, prev[symbol], spread, ts))
    prev[symbol] = spread
```
The insight to state: *"'Changed from the last one' means I need the previous value per
symbol, not globally — the AAPL update at 09:30:02 must compare to the AAPL update at
09:30:01, not to the MSFT line in between."* Candidates who keep one global `prev` get this
silently wrong, and nothing in the output looks obviously broken.

**400 million lines**: stream with a generator. All four questions above survive streaming —
latest-per-symbol, running sums, running max, and previous-value-per-symbol are each O(1)
state per symbol. Memory is O(distinct symbols), not O(lines). **Say that explicitly** —
it's the reason this feed scales and a median wouldn't.

---

## B2 — ranking
```python
value = defaultdict(float)
for symbol, size, price in trades:
    value[symbol] += size * price
top3 = heapq.nlargest(3, value.items(), key=lambda kv: kv[1])
```
1. **Ties** — ask whether they want all tied symbols or a deterministic cut. A stable tiebreak
   (e.g. alphabetical by symbol) makes output reproducible, which matters more than it sounds
   for anything that gets diffed or reconciled.
2. **Top 3 by trade count** — same shape, `counts[symbol] += 1`. Note out loud that this is
   the *same code with a different accumulator*, and that the two rankings usually differ:
   many small trades vs few huge ones.
3. **Per hour** — key on `(hour, symbol)`, or a dict of hour → dict of symbol → value, then
   rank within each hour. Mention that memory is now O(hours x symbols).
4. **500,000 symbols** — aggregation is O(n) regardless. The ranking is where it matters:
   sorting is O(S log S) ≈ 500k x 19; `nlargest(3)` is O(S log 3). **Say the real conclusion
   honestly**: the aggregation pass dominates either way, so this is a micro-optimization
   unless the ranking runs repeatedly. Knowing when an optimization *doesn't* matter is
   worth as much as knowing how to do it.
