# Build the Order Book (Pseudo Code)

This is the "paired coding on order-book content" round. An interviewer would reveal it one
step at a time, so do it that way: **finish each step and trace it before reading the
next.**

Pseudo code is acceptable. Simple Python is better. You don't need classes, heaps, or
anything fancy: **a dict holding two lists is a perfectly good order book.**

Answers: `03_build_the_book_answers.md`. Time: ~60 min total.

---

## Step 1: Representation (5 min, talk only)
> "How would you represent an order? How would you represent the book?"

Decide what fields an order needs. Decide how you'll keep each side in priority order. Say
**why** out loud. What does "best" mean on each side, and where will it live in your list?

---

## Step 2: Top of book (5 min)
Write `best_bid(book)`, `best_ask(book)`, and `spread(book)`.

What do you return when a side is empty?

---

## Step 3: Add an order WITHOUT matching (10 min)
Write `rest(book, order)`: put an order on the correct side, in the correct position.

- Bids: highest price first. Asks: lowest price first.
- **Same price: the new order goes behind the existing ones** (time priority).

Trace: rest a bid @ 15, then a bid @ 14, then a bid @ 15. What's the order in the list?

---

## Step 4: Matching (20 min) ← the main event
Write `submit(book, order)` that:
- matches the incoming order against the opposite side using price-time priority,
- trades at the **resting** price,
- handles partial fills on both sides,
- rests any leftover,
- **returns a list of trades** (buyer, seller, qty, price).

Then trace it, without running it, on the primer's partial-execution example:
```
BIDS: 100 @ 15.00, 50 @ 14.00      ASKS: 100 @ 16.00, 50 @ 17.00
Incoming: Bob SELLS 200 @ 14.00
Expected: trades 100 @ 15.00 and 50 @ 14.00; Bob's 50 rests as an ask @ 14.00
```

---

## Step 5: Cancel (5 min)
Write `cancel(book, order_id)`. Return True if found and removed, False otherwise.

Follow-up: what's the cost of your cancel? If the interviewer says "cancels are 90% of all
messages", how would you make it faster? (Verbal answer is fine.)

---

## Step 6: Print the book (5 min)
Print it the way the primer does, bids and asks side by side:
```
Bid Qty | Bid Px || Ask Px | Ask Qty
    100 |  15.00 ||  16.00 |     100
     50 |  14.00 ||  17.00 |      50
```
Hint: the two sides can have different lengths.

---

## Step 7: Analyze the trades (10 min)
Given the list of trades your engine produced over the day, compute:
1. Total volume traded.
2. **VWAP** (volume-weighted average price) = Σ(qty × price) / Σ qty.
3. Total shares **bought** and **sold** by each trader (a dict).

---

## Verbal follow-ups (be ready for any of these)
1. What's the time complexity of `rest` and `submit` in your design?
2. If the book has 10,000 orders at a few hundred prices, how could you make adding orders
   faster? (Name an idea; no code needed.)
3. How would you support **many stocks** at once?
4. Why might storing prices as floats like `16.1` be risky? What would you do instead?
5. What should `submit` do if it gets an order with qty 0, a negative price, or a side
   that's not BUY/SELL?
6. Two orders arrive "at the same time". How does the exchange decide which is first?
