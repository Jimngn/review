# Answer Key — Mock 5 (Order Book Core)

Full working code: **`../reference/order_book_mock5.py`** — the core only, with nothing from
Mock 6 in it. Verified against all four worked examples in Jane Street's primer by
`../reference/test_mock5.py`; run `python3 test_mock5.py` from that directory.

(Mock 6's escalations live in a separate file, `order_book_mock6.py`. Don't open it while
you're still working on Mock 5 — it carries market orders, IOC/FOK, modify and self-trade
prevention, and it makes the core much harder to see.)

**Read this key as "what to say," not just "what to type."** This round is scored on
reasoning out loud at least as much as on code.

---

## Part 0 — the clarifying conversation

Questions that actually buy you something:

| Question | Why it pays off |
|---|---|
| "Does a trade happen at the incoming order's price or the resting order's?" | **The single highest-value question in this interview.** The primer says resting. Asking proves you've thought about it; getting it wrong silently is the classic failure. |
| "Should I support order IDs now, so cancel is cheap later?" | Signals you expect the escalation. Saves a refactor in Part 5. |
| "Can I store prices as integer cents?" | Shows you know float comparison is unsafe in a system whose entire job is comparing prices. |
| "If an order can't fully fill, does the remainder rest or get cancelled?" | Separates limit from IOC/market behavior before it's asked. |
| "One symbol or many?" | Scopes the problem. Usually they'll say one — take the simplification. |

Say explicitly: *"I'll start with one symbol and limit orders only, and keep the matching
logic in one place so I can reuse it when you add order types."* That sentence alone
signals you've done this before.

---

## Part 1 — data structures

**The answer they're looking for: a dict from price to a FIFO queue of orders, per side.**

```python
from collections import deque
levels = {BUY: {}, SELL: {}}      # side -> {price_in_cents: deque[Order]}
```

Justify each layer out loud — this is the "choosing data structures" bullet you were warned
about:
- **dict keyed by price** → O(1) to find a price level. Prices are sparse; an array indexed
  by price would waste space and break on wide price ranges.
- **deque at each level** → time priority is FIFO, and `popleft()` is O(1). A list would make
  `pop(0)` O(n). Naming this trade-off unprompted is worth real points.
- **best price** = `max(bids)` / `min(asks)`, which is O(P) over distinct price levels. **Say
  this cost out loud and name the upgrade**: a heap (O(log P), but awkward to iterate in
  order and needs lazy deletion of emptied levels) or a sorted-dict/balanced tree (O(log P)
  *and* ordered iteration — what real exchanges use).

Honest framing to use: *"I'll start with max over the keys because it's simple and correct;
if the book gets wide, I'd swap in a heap or a sorted container, and here's the trade-off."*
Interviewers consistently prefer that to a candidate who reaches for a heap immediately and
then fumbles the lazy-deletion bookkeeping.

**Why not simpler alternatives** (be ready, they may ask):
- *One flat list sorted on every insert* — correct but O(n) per insert and O(n log n) if you
  re-sort; fine for a first pass, say so and move on.
- *Two heaps of orders (not levels)* — matching works, but cancel and depth-at-a-price both
  become painful, and you can't print the book without draining the heap.

---

## Part 2 — print the book

Aggregate by price level; don't print one row per order. The whole point of a book display
is total size available at each price.
```python
bids = sorted(level_qty[BUY].items(), reverse=True)   # best (highest) first
asks = sorted(level_qty[SELL].items())                # best (lowest) first
```
Print asks top-down worst-to-best so the two best prices meet in the middle at the spread —
that's how every real book display is laid out, and saying why earns a nod.

---

## Part 3 — matching

The loop, in plain English before you write it: *"While the incoming order still has
quantity and the best opposite price crosses my limit, take the oldest order at that best
price, trade the smaller of the two quantities at the resting price, and remove the resting
order if it's exhausted."*

```python
while incoming.qty > 0:
    best = self.best_ask() if incoming.side == BUY else self.best_bid()
    if not crosses(incoming.side, incoming.price, best):
        break
    resting = front_order_at(other_side, best)
    traded = min(incoming.qty, resting.qty)
    print(f"TRADE {traded} @ {resting.price}")     # <-- RESTING price
    incoming.qty  -= traded
    resting.qty   -= traded
    if resting.qty == 0:
        remove resting from its level
```

Three things that must be right, and that you should point at as you write them:
1. **Cross condition.** Buy crosses when `limit >= best_ask`; sell crosses when
   `limit <= best_bid`. Note it's `>=`, not `>` — equal prices trade.
2. **Trade price is `resting.price`.** Repeat it out loud when you type it.
3. **`min(incoming.qty, resting.qty)`** is what makes partial fills fall out for free in
   Part 4 — mention that you've already handled the next question.

**Manual trace to have ready** (Part 3's test sequence):
```
add BUY  15.00 x100   -> no asks, rests.           Book: B[1500]=100
add SELL 16.00 x100   -> best_bid 1500 < 1600, no cross, rests.
                                                   Book: B[1500]=100  A[1600]=100
add SELL 15.00 x100   -> best_bid 1500 >= 1500 CROSS
                         traded = min(100,100) = 100 @ 1500 (resting bid's price)
                         both exhausted; incoming.qty = 0, doesn't rest
                                                   Book: A[1600]=100
```

---

## Part 4 — partial fills and sweeping

If your Part 3 loop is written as above, **this part requires no new code** — the `while`
already re-picks the best price each pass, and the leftover already rests. Say that out
loud; "my design already handles that, let me prove it" is a strong moment.

Verified trace of the primer's example:
```
Book: B[1500]=100, B[1400]=50 | A[1600]=100, A[1700]=50
add SELL 14.00 x200

pass 1: best_bid 1500 >= 1400 -> trade min(200,100)=100 @ $15.00   rem 100
pass 2: best_bid 1400 >= 1400 -> trade min(100, 50)= 50 @ $14.00   rem  50
pass 3: no bids left -> exit loop
        rem 50 rests as an OFFER at 14.00
Book: A[1400]=50, A[1600]=100, A[1700]=50
```
That matches the primer's final table exactly, including the unintuitive part: **the book
is now one-sided and the resting offer sits at $14.00, below the $16.00 offer.** If your
output differs, your leftover-rests logic is wrong.

---

## Part 5 — cancel

**The naive version** — scan the level's deque and remove the order — is O(n) in the level's
size. It's an acceptable first answer *if you name the cost*.

**The O(1) answer they're fishing for** has two halves, and you should state both:
1. A **dict from order_id to the order object** so you can reach it without searching.
2. A way to **unlink it without shifting** the rest of the queue. Two standard options:
   - **Lazy deletion** (what the reference uses): flag the order `active = False` and
     subtract its quantity from the level total. Matching skips tombstones when it pops.
     O(1) cancel; the cost is that dead objects linger until matching walks past them.
   - **Doubly-linked list per price level** instead of a deque: with a pointer to the node,
     unlinking is O(1) with no tombstones. **This is what production exchanges do**, and
     naming it is the strongest possible answer here.

Keep a running `level_qty[price]` so an emptied level can be deleted immediately — otherwise
`best_bid()` happily returns a price level containing nothing but cancelled orders. That bug
is subtle and a great thing to mention before they find it.

Edge cases to state: unknown ID, double cancel, and cancel-after-full-fill should all be the
same harmless no-op returning `False`, not an exception — the order simply isn't resting
anymore, and the caller can't always know that.

---

## Part 6 — complexity answers, ready to recite

Let **n** = orders consumed by a match, **P** = distinct price levels, **m** = orders at one level.

| Operation | Cost | Say this |
|---|---|---|
| Add, no cross | O(P) with `max()`; O(1) with a cached best price; O(log P) with a heap | "Dominated by finding the best opposite price." |
| Add, crossing | O(n + P) | "Proportional to how many resting orders it eats — each one is removed exactly once, so it's amortized, not quadratic." |
| Cancel | O(1) with id→order map + lazy delete or linked list | "O(m) if I scan; here's how I'd make it O(1)." |
| best_bid / best_ask | O(P) with `max()`, O(1) cached, O(log P) heap | — |
| depth(price) | O(1) with a maintained running total | "I keep a per-level total so I don't sum the queue." |

**The amortization point is worth making unprompted**: a single order might sweep a thousand
resting orders, but each resting order can only be consumed once over its lifetime, so the
*average* cost per order stays small.

**"What if it had to handle a million orders a second?"** — have 3 answers ready:
1. Integer cents, and **fixed-size arrays indexed by price tick** rather than hash maps,
   since real books only trade within a narrow band around the touch.
2. Pre-allocated order objects / object pools to avoid allocation in the hot path.
3. Avoid the `max()` scan entirely by caching the best price and updating it incrementally.
Also fair and honest: *"I'd profile before guessing."*

---

## The three mistakes that sink this question
1. **Trading at the incoming order's price.** Re-read the primer line: the trade occurs "at
   the price of the order that was already listed on the exchange."
2. **Losing time priority** by using a list and inserting/removing from the wrong end, or by
   re-sorting a level and destroying arrival order.
3. **Going quiet during Part 3.** The matching loop takes a few minutes to write; narrate it
   continuously or the interviewer has nothing to score.
