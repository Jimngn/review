# Coding Problems: Trade Data Analysis

Ten problems in the shape of your last round: a short ask, then follow-ups that each add one
twist. Write them in a plain text file. **Don't run them.** Trace by hand. 10–20 min each.

Answers: `01_answers.md`.

Unless a problem says otherwise, trades look like:
```python
{"id": 1, "trader": "A", "symbol": "AAPL", "side": "BUY", "qty": 100, "price": 150.00}
```

---

## 1. Parse a trade file
You get a list of strings, one trade per line:
```
"1,A,AAPL,BUY,100,150.00"
"2,B,MSFT,SELL,50,300.00"
```
Write `parse_trades(lines)` that returns a list of trade dicts with the right types.

**Follow-up:** some lines are bad, like `"3,C,AAPL,BUY,abc,150.00"`, `"4,D,AAPL"`, or an
empty line. Don't crash. Return the good trades **and** a list of `(line_number, reason)`
for the bad ones.

---

## 2. Volume per symbol
Write `volume_by_symbol(trades)` that returns `{symbol: total qty}`.

**Follow-up A:** return the most-traded symbol. What if two symbols tie?
**Follow-up B:** return symbols sorted by volume, highest first.

---

## 3. Net position per trader
Buys add to a position, sells subtract. Write `positions(trades)` that returns
`{(trader, symbol): net_qty}`.

**Follow-up A:** which traders are **flat** (net 0) in every symbol they traded?
**Follow-up B:** why might you key by `(trader, symbol)` instead of a dict inside a dict?
Either is fine. Say the trade-off.

---

## 4. VWAP per symbol
Write `vwap_by_symbol(trades)` that returns `{symbol: VWAP}`, where
VWAP = Σ(qty × price) / Σ qty.

**Follow-up:** why not just average the prices? Give a two-trade example where the two
answers are very different.

---

## 5. Validate trades
Write `validate(trades, allowed_symbols)` that returns a list of `(trade_id, reason)` for
every problem found. Rules:
- side must be `"BUY"` or `"SELL"`
- qty must be a positive integer
- price must be > 0
- symbol must be in `allowed_symbols`
- trade IDs must be unique (report the **second** occurrence as a duplicate)

A trade can have more than one problem. Report all of them.

**Follow-up:** a trade's price is 10x the average price for its symbol. Is that an error?
How would you flag it without rejecting it?

---

## 6. Top of book from a snapshot
You get a list of resting orders (no matching needed):
```python
{"id": 7, "side": "BUY", "price": 15.00, "qty": 100}
```
Write `top_of_book(orders)` that returns `(best_bid, best_ask)`. Use `None` for an empty side.

**Follow-up A:** also return the **total quantity** at the best bid and at the best ask.
**Follow-up B:** write `is_crossed(orders)`. If a snapshot from our market data is crossed,
what does that tell you? (Think about Rule 1 of the primer.)

---

## 7. Reconcile our trades vs the exchange's
You have `ours` and `theirs`, two lists of trades for the same day. Match them by `id`.
Write `reconcile(ours, theirs)` that returns:
- IDs the exchange has that **we're missing**
- IDs we have that the **exchange doesn't**
- IDs in both where `qty`, `price`, or `side` **differ**

**Follow-up:** what's the time complexity if you compare with nested loops? How do you make
it O(n)?

---

## 8. Position limit breach
Each trader may hold at most `limit` shares long **or short** per symbol. Process trades in
order and return the **ID of the first trade** that pushes any trader's position past the
limit (absolute value > limit). Return `None` if no trade does.

**Follow-up:** instead of the first one, return **every** breaching trade. Should a trade
that moves a position from −600 to −550 (limit 500) count as a breach? Discuss.

---

## 9. O(n) sort for a short array
> "Sort this list of trade sizes. Every size is a whole number from 1 to 10."
> `[3, 1, 10, 3, 7, 1, 1]`

Do it in **O(n)** without `sort()`.

**Follow-up:** why is this faster than O(n log n)? When would it be a bad idea?
**Follow-up:** "The array has only 5 elements." What simple sort would you write instead?

---

## 10. Merge two time-sorted trade streams
Two exchanges each send you trades already sorted by `time` (an int). Write
`merge(a, b)` that returns one list sorted by time, **without** calling `sort()`.

**Follow-up:** what if there are k exchanges instead of 2? (Verbal.)
