# Mock 5 — Order Book / Matching Engine (CORE, ~60 min)

This is the single most likely long-form question in the final round, and Jane Street
telegraphed it by sending you `Resource/Order_20Book_20Basics_20Primer.pdf`. **Re-read that
primer before starting this mock.** The interviewer will assume you know its vocabulary:
*bid, offer, cross, resting order, price-time priority, partial execution*.

## How to run this one
- Set a **60-minute timer.** Do not pause it between parts.
- **Do not read ahead.** Each part is revealed only after the previous one works — that's
  how the real escalation goes, and reading ahead lets you over-engineer Part 1, which is
  the most common way candidates lose this round.
- Talk out loud continuously. Narrate your data-structure choice *before* you type it.
- Keep a scratch area for your manual traces — you may be asked to prove correctness
  without running the code.

---

## Part 0 — the clarifying conversation (5 min, before any code)
> "We're going to build a simple exchange. It takes in bids and offers and matches them.
> Let's start simple and build up."

**Stop. Ask your questions now.** Come up with at least four of your own before you look at
the answer key's list. Strong candidates establish at minimum:
- Single security, or multiple symbols?
- Are prices integers, decimals, or should I use cents to avoid float issues?
- Does an incoming order that can't fully match rest on the book, or get cancelled?
- At what price does a trade execute — the incoming order's or the resting order's?
- Do I need to support order IDs for later cancellation?

That last one matters a lot: **if you ask about order IDs now and design for them, Part 5
(cancel) costs you two minutes instead of a rewrite.** Asking good questions here is not
politeness — it's cheap insurance against a mid-interview refactor.

---

## Part 1 — represent an order and the book (10 min)
> "Let's say an order has a side — buy or sell — a price, and a quantity. Set up a way to
> represent an order, and a way to represent the book itself."

Write the data structures. Before you type, say out loud:
- What structure holds the bids, and what holds the offers?
- How will you find the **best** bid (highest price) and **best** offer (lowest price)?
- At a single price, multiple orders can rest. What preserves their arrival order?

Then write `add_order(side, price, qty)` that **just rests the order on the book** — no
matching yet. Confirm with the interviewer that's an OK intermediate step.

---

## Part 2 — print the book (5 min)
> "Show me the state of the book."

Write `print_book()`. Output offers above bids, best prices innermost, in the primer's
shape:
```
ASK  $17.00   50
ASK  $16.00  100
---------------
BID  $15.00  100
BID  $14.00   50
```
State out loud: offers ascend going up, bids descend going down, and the gap in the middle
is the spread. Aggregate quantity at each price level — don't print one line per order.

---

## Part 3 — matching (20 min, the heart of it)
> "Now make it actually match. When an order comes in that crosses the book, it should
> trade."

Write the matching logic inside `add_order`. Requirements, exactly as the primer defines:
- A bid and an offer **cross** when bid price >= offer price.
- The trade executes **at the resting order's price**, not the incoming order's.
- Ties at the same price are broken by **time priority** — oldest resting order first.
- Print each trade as it happens.

Test against this sequence and verify by hand before running anything:
```
add_order(BUY,  15.00, 100)
add_order(SELL, 16.00, 100)      # no trade — no cross
add_order(SELL, 15.00, 100)      # trades 100 @ $15.00
```

---

## Part 4 — partial fills and sweeping multiple levels (10 min)
> "What happens if someone sends a big order that's bigger than what's resting?"

Extend matching so that one incoming order can:
- fill against **several** resting orders at the same price (time priority),
- **sweep through several price levels** (best price first),
- and if quantity remains after exhausting all crossing levels, **rest the remainder** on
  the book.

This is the primer's partial-execution example — reproduce it exactly:
```
Book:  BID 100 @ $15.00,  BID 50 @ $14.00
       ASK 100 @ $16.00,  ASK 50 @ $17.00

add_order(SELL, 14.00, 200)
```
Expected: trade 100 @ $15.00, then trade 50 @ $14.00, then **50 shares rest as an offer at
$14.00**. Trace it by hand first; then confirm your book matches the primer's final table.

---

## Part 5 — cancel (10 min)
> "Traders change their minds. Add the ability to cancel an order."

Change the signature so orders carry an ID: `add_order(order_id, side, price, qty)`, and
write `cancel(order_id)`.

Be ready to answer, out loud:
- What's the time complexity of your cancel? If you're scanning a list to find the order,
  say so honestly and name what it costs.
- What would you change to make cancel **O(1)**? (Think: what do you need to go straight to
  the order, and what structure lets you unlink it without shifting everything else?)
- What happens if the ID doesn't exist, or was already fully filled?

---

## Part 6 — the complexity conversation (closing 5 min)
Expect to be asked, and have crisp answers ready:
- What is the cost of adding a non-crossing order? Of an order that sweeps the book?
- Why is the cost of matching naturally bounded by "orders consumed" rather than book size?
- What's in your book: a sorted list, a heap, or a dict of price levels — and **why**?
  Name the trade-off you accepted.
- If this had to handle a million orders a second, what's the first thing you'd change?

---

## Self-scoring
Mark honestly before reading the key:
- [ ] Asked about execution price (resting vs incoming) **before** writing matching code
- [ ] Trades printed at the **resting** order's price
- [ ] Time priority actually enforced (FIFO within a price level)
- [ ] Partial fill rests the remainder, with correct leftover quantity
- [ ] Multi-level sweep works in best-price-first order
- [ ] Stated a complexity for every operation, unprompted
- [ ] Never went silent for more than ~20 seconds
