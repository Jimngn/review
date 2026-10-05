# Order Book Scenarios: Hand-Trace Drills

This is the core of the primer round. For each scenario, write down on paper or in a txt
file, out loud:

1. **Which side** the incoming order looks at, and in what order.
2. **Every trade:** buyer, seller, quantity, **price**.
3. **The book afterward** (both sides, in priority order).
4. **Sanity check:** best bid < best ask?

Rules reminder: equal or crossed prices trade · trade at the **resting** price · price first,
then time · leftover rests at its own limit.

Answers: `02_scenarios_answers.md`. Aim for under 3 minutes each.

Notation: `#id trader qty @ price`. Within the same price, orders are listed in arrival
order (earlier first).

---

### Scenario 1: No trade
```
BIDS                  ASKS
A 100 @ 15.00         B 100 @ 16.00
```
**Incoming:** C **sells** 50 @ 15.50.

Also give the best bid, best ask, and spread afterward.

---

### Scenario 2: Equal prices
Same starting book as Scenario 1.
**Incoming:** C **buys** 100 @ 16.00.

---

### Scenario 3: The price trap
Same starting book as Scenario 1.
**Incoming:** C **buys** 100 @ 18.00.

What price does C pay? Who is happier with the outcome, and why is that the rule?

---

### Scenario 4: Sweep two levels, then rest
```
BIDS                  ASKS
A 100 @ 15.00         B  50 @ 16.00
                      C 100 @ 16.50
                      D 200 @ 17.00
```
**Incoming:** E **buys** 250 @ 16.50.

---

### Scenario 5: Time priority + partial fill of a resting order
```
BIDS                  ASKS
(empty)               Anne 100 @ 16.00   (arrived 1:30pm)
                      Bob  200 @ 16.00   (arrived 2:30pm)
                      Cat  100 @ 17.00
```
**Incoming:** You **buy** 150 @ 16.00.

Then: Dan sends a **sell** 100 @ 16.00. Where does Dan go in the queue relative to Bob?

---

### Scenario 6: A sell sweeping bids
```
BIDS                  ASKS
A 100 @ 15.00 (1st)   D 100 @ 16.00
B 100 @ 15.00 (2nd)
C 300 @ 14.00
```
**Incoming:** E **sells** 250 @ 14.50.

Careful: why doesn't E trade with C?

---

### Scenario 7: A full sequence from an empty book
Process these **in order**, starting from an empty book. Write the book and any trades after
**each** one.

| # | Trader | Side | Qty | Price |
|---|---|---|---|---|
| 1 | A | BUY  | 100 | 10.00 |
| 2 | B | BUY  |  50 | 10.10 |
| 3 | C | SELL |  80 | 10.20 |
| 4 | D | SELL | 120 | 10.00 |
| 5 | E | BUY  | 100 | 10.30 |
| 6 | F | SELL |  30 | 10.30 |

At the end, give the full list of trades and the total volume traded.

---

### Scenario 8: Cancels
```
BIDS                  ASKS
(empty)               Anne 100 @ 16.00 (1st)
                      Bob  100 @ 16.00 (2nd)
```
1. Anne **cancels** her order.
2. You **buy** 100 @ 16.00. Who do you trade with?
3. Verbal: if instead of cancelling, Anne had **reduced** her order to 50, and Bob had
   **increased** his to 300, who keeps their place in line? *(Beyond the primer. Reason it
   out.)*
4. Verbal: Anne sends a cancel at the exact moment your buy arrives. What can happen?

---

### Scenario 9: Bigger than the whole other side
```
BIDS                  ASKS
(empty)               A 100 @ 16.00
                      B 100 @ 17.00
```
**Incoming:** C **buys** 500 @ 20.00.

What's the book afterward? Is anything wrong with a book that has only bids?

---

### Scenario 10: Work backward
A single incoming **sell** order produced exactly these trades, in this order:
```
100 shares @ 15.00
 50 shares @ 14.00
```
Nothing else traded. What can you say for sure about the sell order's **price** and
**quantity**? What did the bid side probably look like before? What might be on the book
afterward?

---

## Concept checks (rapid-fire, answer out loud in 1–2 sentences)

1. What's the difference between a bid and an offer?
2. Bid 100 @ $10 means the buyer will pay what range of prices?
3. Can the book ever be crossed after an order is fully processed? Why not?
4. Two offers at the same price: which trades first?
5. A $16 offer arrived at 9:30am and a $15.50 offer arrived at 10:00am. Which trades first
   against an incoming buy @ $17?
6. Why can one order produce many trades at different prices?
7. A resting order gets partially filled. Does it lose its time priority?
8. What's the spread, and what does a wide spread tell you?
9. The primer says "the offer never truly shows up on the order book". What does that mean?
10. If you're a buyer, why would you ever send a bid **below** the best ask instead of just
    paying the ask?
