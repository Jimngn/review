# Mock 6 — Order Book Extensions (the escalation, ~45 min)

**Prerequisite:** a working matching engine from Mock 5. Start this mock with that code
already on screen, exactly as the interviewer would after you finished the core.

The point of this mock is that each part arrives **cold, one at a time, on top of code you
already wrote.** That's the actual difficulty of this round — not any single feature, but
whether your Part 3 design survives Part 7 without a rewrite. If you find yourself needing
to tear something down, say so out loud and explain the trade-off; that's a much better
look than silently hacking around it.

---

## Part 1 — best bid / best offer (5 min)
> "Add a way to report the best bid and the best offer."

Write `best_bid()` and `best_ask()`. Then:
- What do they return when that side of the book is **empty**? Decide and justify.
- What's the complexity? If it's O(number of price levels) because you're calling `max()`
  over dict keys, say that out loud and name the alternative.
- Add `spread()`. What's the spread when one side is empty?

---

## Part 2 — depth at a price, and the aggregated book (10 min)
> "Now I want the total size resting at each price."

Write `depth(side, price)` → total quantity resting at that price, and `book_snapshot()` →
the aggregated levels, best-first:
```
[(15.00, 150), (14.00, 50)]     # bids, descending
[(16.00, 100), (17.00, 50)]     # asks, ascending
```
Follow-up to be ready for: *"Can you give me just the top 3 levels per side?"* — note how
this connects straight back to the top-k question from Mock 1. If your prices live in a
heap, pulling the top 3 **in order** is not free; say what it costs.

---

## Part 3 — modify quantity (10 min)
> "Let a trader change the quantity of a resting order."

Write `modify_qty(order_id, new_qty)`. The rule the interviewer is probing for:
- **Decreasing** quantity keeps the order's place in the queue (time priority preserved).
- **Increasing** quantity sends it to the **back** of the queue at that price.

Say out loud *why* that asymmetry exists before you implement it — the reasoning (you
can't gain queue priority you didn't earn, but giving up size costs nobody) is the actual
answer they want. Also handle: what does `new_qty == 0` mean?

---

## Part 4 — modify price (10 min)
> "Now let them change the price."

Write `modify_price(order_id, new_price)`. Changing price means losing queue position —
the order moves to the **back** of the queue at the new price.

Critical follow-up, and candidates miss this: **what if the new price now crosses the
book?** Should it immediately trade? Argue a position and implement it. The clean
implementation is cancel-then-add, reusing your existing `add_order` so matching comes for
free — if you see that, say it out loud, because reuse is exactly what they're watching for.

---

## Part 5 — market orders (5 min)
> "Add a market order — it has no price, it just wants to trade right now."

Write `add_market_order(order_id, side, qty)`. Decide and defend:
- What happens to quantity that can't be filled because the book runs dry? (It must **not**
  rest — a market order has no price to rest at.)
- What if the opposite side is completely empty when it arrives?

---

## Part 6 — immediate-or-cancel and fill-or-kill (10 min)
> "Add an order that fills whatever it can right away and cancels the rest."

Write IOC. Then the harder sibling:
> "Now fill-or-kill — it either fills completely or does nothing at all."

FOK is the interesting one: you can't just start matching and bail halfway, because you'd
have already printed trades. State the solution out loud — **check available crossing
quantity first, then execute only if it's sufficient** — and note the cost of that extra
pass.

---

## Part 7 — self-trade prevention (5 min)
> "What if the same trader is on both sides — their own bid matches their own offer?"

Add a `trader_id` to orders and prevent self-matching. There's no single right answer, so
name the options and pick one:
- cancel the resting order and keep matching onward,
- cancel the incoming order,
- cancel the smaller of the two and continue with the remainder.
Say which real exchanges care about this and why (wash trades are a regulatory problem).

---

## Part 8 — rapid-fire edge cases (verbal, 5 min)
Answer each in one or two sentences, out loud, no code:
1. An order arrives with **quantity zero**. What do you do?
2. An order arrives with **negative quantity** or a **negative price**?
3. A **duplicate order ID** arrives while the original is still resting.
4. `cancel()` is called twice on the same ID.
5. `cancel()` is called on an order that was **already fully filled**.
6. Prices are floats: `0.1 + 0.2 != 0.3`. What breaks, and what's the standard fix?
7. The incoming order crosses, but the resting order at that level has quantity 0 left
   because of a bug — would your loop terminate?
8. Two orders at the same price arrive in the same **microsecond**. What breaks the tie?

---

## Self-scoring
- [ ] Reused `add_order` for modify-price instead of duplicating matching logic
- [ ] Got the decrease-keeps-priority / increase-loses-priority rule right **and explained why**
- [ ] Market order leftover does not rest on the book
- [ ] Named the pre-check pass for FOK without being walked to it
- [ ] Answered the float-precision question with "use integer cents / ticks"
- [ ] Gave a complexity for every new method, unprompted
