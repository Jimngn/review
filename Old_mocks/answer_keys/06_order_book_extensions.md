# Answer Key — Mock 6 (Order Book Extensions)

Working code for every part: **`../reference/order_book_mock6.py`**, verified by
`../reference/test_mock6.py`.

That file is standalone — it repeats the Mock 5 core so it reads top to bottom — and every
addition is marked with a `# +++ MOCK 6 +++` banner, so you can see exactly what each
escalation cost in lines. Compare it against `order_book_mock5.py` to see the diff.

---

## Part 1 — best bid / best offer
```python
def best_bid(self): return max(self.levels[BUY])  if self.levels[BUY]  else None
def best_ask(self): return min(self.levels[SELL]) if self.levels[SELL] else None
```
**Empty side → `None`**, not 0 and not an exception. Justify it: 0 is a *valid price* and
would look like a real bid at zero, which would then appear to cross every offer. That
reasoning is the answer; the code is trivial.

**Spread** is `None` when either side is empty — a one-sided book has no spread. Candidates
who return a huge number or crash here get caught by the follow-up.

Complexity: `max()` over dict keys is O(P). The honest line: *"O(P) in distinct price levels.
In production I'd cache the best price and update it on insert and on level removal, making
it O(1) reads — the only cost is bookkeeping when the best level empties out."*

---

## Part 2 — depth and snapshot
Keep a `level_qty[side][price]` running total updated on every rest, fill, and cancel. Then
`depth()` is O(1) instead of summing a queue.

```python
def snapshot(self, levels=None):
    bids = sorted(self.level_qty[BUY].items(), reverse=True)
    asks = sorted(self.level_qty[SELL].items())
    return bids[:levels], asks[:levels]
```
**"Just the top 3 levels"** — connect it to Mock 1 out loud: *"This is top-k again. Sorting
all levels is O(P log P); if P were large and k small I'd use `heapq.nlargest(k, ...)` for
O(P log k), or keep the levels in a sorted structure so the top k is just the first k."*
Making that link unprompted shows the interviewer you're seeing structure, not memorizing
problems.

---

## Part 3 — modify quantity
```python
if new_qty < order.qty:       # shrink: keep queue position
    level_qty[side][price] -= (order.qty - new_qty)
    order.qty = new_qty
else:                         # grow: cancel and re-add at the back
    cancel(order_id); rest(new order with new_qty)
```
**Say the reasoning before the code:** *"Shrinking gives up size, which costs the other
traders in the queue nothing, so there's no reason to punish it. Growing is effectively a
new order — if increasing size kept your place, you'd post a 1-lot early to camp at the
front of the queue and inflate it later, which is exactly the gaming the rule prevents."*

That "why" is the whole question. The code is five lines.

`new_qty == 0` → treat as a cancel. `new_qty < 0` → reject.

---

## Part 4 — modify price
```python
def modify_price(self, order_id, new_price):
    order = self.orders.get(order_id)
    if order is None: return False
    side, qty, trader = order.side, order.qty, order.trader
    self.cancel(order_id)
    self.add_order(order_id, side, new_price, qty, trader)   # reuse -> matching is free
```
**Lead with the reuse observation**: *"A reprice is just a cancel plus an add. If I route it
through `add_order`, then a reprice that crosses the book trades immediately with no new
code."* Verified: repricing a $17.00 offer down to $15.00 against a resting $15.00 bid trades
100 @ $15.00 — at the **resting bid's** price, because the repriced order is the incoming
one.

Watch the ordering trap: cancel **before** re-adding. If you add first, the duplicate-ID
guard fires, or you briefly have the same order resting twice and it can trade with itself.

---

## Part 5 — market orders
```python
order = Order(id, side, price=None, qty=qty)
self._match(order)       # note: NO self._rest() afterwards
```
Represent "no limit" as `price=None` and make the cross check return `True` for it — that
way market orders flow through the exact same matching loop. One code path, not two.

**The leftover must not rest.** State why: a resting order needs a price, and a market order
by definition doesn't have one. Real exchanges either cancel the remainder or reject the
order outright; name both.

Empty opposite side → zero trades, nothing rests, no error. Verified.

---

## Part 6 — IOC and FOK
**IOC** is the easiest add in the whole mock: it's the limit-order path minus the final
`_rest()` call. If you structured matching and resting as separate steps in Mock 5, this is
one line — and you should point that out, because it's your Part 1 design paying off.

**FOK is the one with a real idea in it.** You cannot start matching and abort halfway,
because the trades you already printed have happened — there's no un-printing an execution.
So:
```python
if self._available_qty(side, limit) < qty:
    return []          # kill: nothing executes
return self._match(order)
```
Walk the crossing levels first, summing quantity, stopping at the first level that doesn't
cross. That's an extra O(P) pass. State the trade-off: *"Two passes instead of one, but
atomicity requires knowing the outcome before committing to any of it."*

If asked to avoid the second pass: you'd have to buffer the trades and only publish them if
the order completes — same idea, different place to pay for it.

---

## Part 7 — self-trade prevention
There is no single correct policy, so **name the menu, then pick and defend one**:
- **Cancel resting (decrement-and-cancel)** — drop your own resting order, keep matching
  down the book. The reference uses this; it's closest to what most exchanges do.
- **Cancel incoming** — the aggressive order is killed; your resting order keeps its place.
- **Cancel both.**

Verified behavior: with two offers at $16.00 (mine first, then another trader's), my own
incoming bid skips mine, cancels it, and fills against the other trader's — and my offer is
gone from the book rather than left resting.

**Say why anyone cares:** trading with yourself produces a real printed trade at a price you
chose, with no change in your position. That's **wash trading** — it fakes volume and can
paint a misleading price. It's a regulatory problem, not just an aesthetic one. Knowing
*that* is what distinguishes a finance-aware answer here.

---

## Part 8 — edge cases, with the answers

1. **Quantity zero** — reject it. An order to trade nothing is meaningless, and if it rests
   it becomes a permanent tombstone at the front of a queue. (Caveat worth voicing: in some
   protocols a quantity-zero *modify* is the idiom for a cancel.)
2. **Negative quantity / negative price** — reject at the boundary. Validate on entry so
   the matching loop can assume clean input; letting a negative quantity into the engine
   corrupts level totals in ways you'll never find by reading the matching code.
3. **Duplicate order ID while the original rests** — reject. The ID is the handle for cancel
   and modify; two live orders sharing one makes both unaddressable.
4. **Double cancel** — no-op returning `False`. Not an exception: the client may have raced
   with a fill and can't know.
5. **Cancel an already-filled order** — identical no-op. The caller genuinely cannot
   distinguish these two cases, so treating them the same is the kind thing *and* the
   correct thing.
6. **Float prices** — `0.1 + 0.2 != 0.3`, and `15.00` may not compare equal to a `15.00`
   that arrived by a different arithmetic path, so orders silently fail to cross. **Fix:
   integer cents, or ticks.** This is a guaranteed-value answer; have it loaded.
7. **A zero-quantity resting order** — if your inner loop trades `min(incoming, resting)`
   and only removes the resting order when it hits exactly 0, a 0-quantity order traps you
   in an infinite loop: it trades 0, nothing decreases, repeat forever. Mention that you
   guard it by removing any order whose quantity reaches `<= 0`, and by validating on entry.
   Spotting a non-termination risk unprompted is a genuinely strong signal.
8. **Same-microsecond arrival** — the exchange assigns a monotonically increasing sequence
   number on receipt; the queue order *is* the tiebreaker. Timestamps are for reporting, the
   sequence is for priority. (Hence `seq` in the reference `Order`.)

---

## What "good" sounds like in this mock
The features are easy. What's being measured is whether you:
- **predict the next escalation** ("I'll keep matching and resting separate, since you'll
  probably want IOC later"),
- **reuse instead of duplicate** (reprice → cancel + add),
- **give the economic reasoning**, not just the mechanical rule (queue priority, wash trades),
- and **volunteer complexity** before being asked, every time.
