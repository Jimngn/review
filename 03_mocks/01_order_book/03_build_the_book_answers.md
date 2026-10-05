# Answers: Build the Order Book

The full code below was run and checked against all four of the primer's worked examples
and every scenario in `02_scenarios.md`. It only uses what's in the Intro to Python PDF:
dicts, lists, loops, if, functions.

---

## Step 1: Representation

**Order:** a dict.
```python
order = {"id": 1, "trader": "Anne", "side": "SELL", "price": 16.00, "qty": 100}
```
- `id` so it can be cancelled. `trader` so trades say who traded. `qty` is the *remaining*
  quantity and goes down as it fills.

**Book:** a dict with two lists, **each kept sorted best-first**.
```python
book = {"bids": [], "asks": []}
```
- `bids[0]` is always the best bid (highest price, earliest at that price).
- `asks[0]` is always the best ask (lowest price, earliest at that price).

Why say this out loud: if the list is always in priority order, matching is simple. **Just
keep looking at index 0.** Time priority comes for free because we insert new orders
*behind* existing ones at the same price, so we don't even need a timestamp field.

---

## Step 2: Top of book
```python
def best_bid(book):
    if len(book["bids"]) == 0:
        return None
    return book["bids"][0]["price"]

def best_ask(book):
    if len(book["asks"]) == 0:
        return None
    return book["asks"][0]["price"]

def spread(book):
    bid = best_bid(book)
    ask = best_ask(book)
    if bid is None or ask is None:
        return None
    return ask - bid
```
Return `None` for an empty side rather than crashing or returning 0 (0 is a real-looking
price, which hides a bug).

---

## Step 3: Rest without matching
```python
def is_better_price(side, price_a, price_b):
    # is price_a strictly more competitive than price_b for this side?
    if side == "BUY":
        return price_a > price_b
    else:
        return price_a < price_b

def rest(book, order):
    if order["side"] == "BUY":
        orders = book["bids"]
    else:
        orders = book["asks"]
    # walk past every order that is at least as good as ours (better price, or same price
    # but earlier); stop at the first one that is strictly worse
    i = 0
    while i < len(orders) and not is_better_price(order["side"], order["price"], orders[i]["price"]):
        i += 1
    orders.insert(i, order)
```
**The key detail is *strictly* better.** At the same price we keep walking, so the new order
lands **behind** existing orders at that price. That's time priority. If you used `>=`, a
new order would jump ahead of older ones at the same price, which is a bug.

Trace: bid 15 → `[15a]`. Bid 14 → 14 isn't better than 15, walk past, end → `[15a, 14]`.
Bid 15 → is 15 better than 15a? no, walk; is 15 better than 14? **yes**, stop at i=1 →
`[15a, 15b, 14]`. ✓

---

## Step 4: Matching
```python
def crosses(incoming, resting):
    if incoming["side"] == "BUY":
        return incoming["price"] >= resting["price"]
    else:
        return incoming["price"] <= resting["price"]

def submit(book, order):
    trades = []
    if order["side"] == "BUY":
        opposite = book["asks"]
    else:
        opposite = book["bids"]

    while order["qty"] > 0 and len(opposite) > 0:
        best = opposite[0]
        if not crosses(order, best):
            break                                  # best price doesn't cross, so nothing worse will

        fill = min(order["qty"], best["qty"])
        if order["side"] == "BUY":
            buyer, seller = order["trader"], best["trader"]
        else:
            buyer, seller = best["trader"], order["trader"]
        trades.append({"buyer": buyer, "seller": seller,
                       "qty": fill, "price": best["price"]})   # RESTING price

        order["qty"] -= fill
        best["qty"] -= fill
        if best["qty"] == 0:
            opposite.pop(0)                        # fully filled, so remove it

    if order["qty"] > 0:
        rest(book, order)                          # leftover rests at its own limit
    return trades
```
Points to say while writing:
- `break` (not `continue`) when the best doesn't cross: the list is sorted, so if the
  *best* resting price doesn't cross, nothing after it will either.
- **Price = `best["price"]`**, the resting order's price. This is the primer's trap.
- A partially filled resting order stays at index 0, so it **keeps its priority**.
- The loop has two exits: incoming fully filled, or opposite side empty / no cross.

**Trace of Bob sells 200 @ 14.00** against bids `[100@15, 50@14]`:
| iter | best | crosses? (bid >= 14) | fill | Bob left | book bids after |
|---|---|---|---|---|---|
| 1 | 100@15 | 15 >= 14 yes | 100 @ 15.00 | 100 | `[50@14]` |
| 2 | 50@14 | 14 >= 14 yes | 50 @ 14.00 | 50 | `[]` |
| 3 | loop ends: bids empty | | | | |
Bob has 50 left, so `rest` puts him on asks: `[50@14, 100@16, 50@17]`. ✓ Matches the primer.

---

## Step 5: Cancel
```python
def cancel(book, order_id):
    for side in ["bids", "asks"]:
        orders = book[side]
        for i in range(len(orders)):
            if orders[i]["id"] == order_id:
                del orders[i]
                return True        # return right away: never keep looping after deleting
    return False
```
- Cost: **O(n)** to find it.
- To make it faster: keep a second dict `orders_by_id = {id: order}`. Then you find the
  order in O(1). Removing it from the middle of the list is still a cost, so real engines
  either use a linked list per price level or just **mark it cancelled and skip it** when it
  reaches the front. Saying "dict from order ID to order for O(1) lookup" is the key idea.

---

## Step 6: Print the book
```python
def print_book(book):
    bids = book["bids"]
    asks = book["asks"]
    print("Bid Qty | Bid Px || Ask Px | Ask Qty")
    rows = max(len(bids), len(asks))
    for i in range(rows):
        if i < len(bids):
            left = f"{bids[i]['qty']:>7} | {bids[i]['price']:>6.2f}"
        else:
            left = f"{'':>7} | {'':>6}"
        if i < len(asks):
            right = f"{asks[i]['price']:>6.2f} | {asks[i]['qty']:>7}"
        else:
            right = f"{'':>6} | {'':>7}"
        print(left + " || " + right)
```
The interviewer cares about `rows = max(...)` and the `if i < len(...)` checks, which
handle uneven sides without an IndexError. Exact spacing doesn't matter. In pseudo code just
say "pad the missing side with blanks".

---

## Step 7: Analyze the trades
```python
def total_volume(trades):
    total = 0
    for t in trades:
        total += t["qty"]
    return total

def vwap(trades):
    total_qty = 0
    total_notional = 0
    for t in trades:
        total_qty += t["qty"]
        total_notional += t["qty"] * t["price"]
    if total_qty == 0:
        return None                     # no trades: avoid dividing by zero
    return total_notional / total_qty

def bought_and_sold(trades):
    result = {}                         # trader -> {"bought": x, "sold": y}
    for t in trades:
        for trader in [t["buyer"], t["seller"]]:
            if trader not in result:
                result[trader] = {"bought": 0, "sold": 0}
        result[t["buyer"]]["bought"] += t["qty"]
        result[t["seller"]]["sold"] += t["qty"]
    return result
```
Scenario 7's trades (50@10.10, 70@10.00, 80@10.20, 20@10.30): volume 220, notional
505 + 700 + 816 + 206 = 2,227.00, **VWAP = 2227 / 220 ≈ 10.123**.

Why VWAP and not the plain average of prices: a 1-share trade at a weird price shouldn't
count as much as a 10,000-share trade.

---

## Verbal follow-ups
1. **Complexity:** `rest` is O(n) (walk the list + insert). `submit` is O(k) for k fills +
   O(n) to rest. `pop(0)` on a Python list is also O(n). Say it; it's fine for an interview.
2. **Faster:** group orders **by price level**: a dict `price → list of orders (FIFO)`
   plus a sorted list of prices (or a heap for best price). Adding at an existing price is
   then O(1). Most orders arrive near the top of the book, so even a simple sorted structure
   works well in practice.
3. **Many stocks:** `books = {"AAPL": new_book(), "MSFT": new_book(), ...}`. Each symbol's
   book is completely independent, which also makes it easy to spread across machines.
4. **Floats:** `0.1 + 0.2 != 0.3` in floating point, so comparing prices for equality can
   fail. Store prices as **integer cents** (or ticks): `1610` instead of `16.10`.
5. **Validate before matching:** reject qty <= 0, price <= 0, unknown side, missing
   fields, and return a reject message instead of touching the book. A bad order should
   never corrupt the book.
6. **Sequencing:** the exchange processes messages **one at a time** in the order it receives
   them. There's no true "same time": whoever the sequencer stamps first is first.

---

## The whole engine in one block (for re-reading the night before)
```python
def new_book():
    return {"bids": [], "asks": []}

# + best_bid, best_ask, spread, is_better_price, rest, crosses, submit, cancel,
#   print_book from above.

book = new_book()
submit(book, {"id": 1, "trader": "you",  "side": "BUY",  "price": 15.00, "qty": 100})
submit(book, {"id": 2, "trader": "Anne", "side": "SELL", "price": 16.00, "qty": 100})
trades = submit(book, {"id": 3, "trader": "Bob", "side": "SELL", "price": 15.00, "qty": 100})
# trades == [{"buyer": "you", "seller": "Bob", "qty": 100, "price": 15.00}]
# book: bids empty, asks Anne 100 @ 16.00     (the primer's first worked example)
```
