# Answers: Order Book Scenarios

Every scenario below was checked by running it through the reference engine in
`03_build_the_book_answers.md`.

---

### Scenario 1: No trade
- C sells @ 15.50, so it looks at **bids**. Best bid = 15.00. Does 15.00 >= 15.50? **No.** No trade.
- C rests on the ask side. 15.50 is better (lower) than 16.00, so it goes **in front**.
```
BIDS                  ASKS
A 100 @ 15.00         C  50 @ 15.50
                      B 100 @ 16.00
```
- Best bid 15.00, best ask **15.50**, spread **0.50** (was 1.00). C *tightened* the market.

---

### Scenario 2: Equal prices
- C buys @ 16.00 and looks at asks. Best ask = 16.00. 16.00 >= 16.00, so they **trade (equal counts)**.
- **Trade: C buys 100 from B @ 16.00.** Both fully filled.
```
BIDS                  ASKS
A 100 @ 15.00         (empty)
```

---

### Scenario 3: The price trap
- C buys @ 18.00, best ask 16.00. 18 >= 16, so they trade.
- **Trade: C buys 100 from B @ 16.00**, B's resting price. **Not 18.**
- Book: `A 100 @ 15.00` on bids, asks empty.
- Who's happier? **C.** C was willing to pay 18 and paid 16 (price improvement). B got
  exactly what B asked for.
- Why the rule: B was there first and publicly committed to 16. The exchange honors the
  displayed price. It's predictable and fair to the order that set the market.

---

### Scenario 4: Sweep two levels, then rest
E buys 250 @ 16.50 and looks at asks, lowest first:
1. B 50 @ 16.00: 16.50 >= 16.00, cross. Fill min(250, 50) = **50 @ 16.00**. B gone. E has 200 left.
2. C 100 @ 16.50: 16.50 >= 16.50, cross. Fill min(200, 100) = **100 @ 16.50**. C gone. E has 100 left.
3. D 200 @ 17.00: 16.50 >= 17.00? **No. Stop.**
4. E's leftover **100 rests as a bid @ 16.50** (its own limit, not 17).

**Trades:** E/B 50 @ 16.00 · E/C 100 @ 16.50
```
BIDS                  ASKS
E 100 @ 16.50         D 200 @ 17.00
A 100 @ 15.00
```
Sanity: 16.50 < 17.00, not crossed. ✓

---

### Scenario 5: Time priority + partial fill
You buy 150 @ 16.00 and look at asks:
1. Anne 100 @ 16.00 (earliest at best price). Fill **100 @ 16.00**. Anne gone. 50 left.
2. Bob 200 @ 16.00. Fill **50 @ 16.00**. Bob has **150 left**. You're done.

**Trades:** you/Anne 100 @ 16.00 · you/Bob 50 @ 16.00
```
BIDS                  ASKS
(empty)               Bob 150 @ 16.00
                      Cat 100 @ 17.00
```
**Dan's sell 100 @ 16.00** doesn't cross (no bids), so it rests **behind Bob** at 16.00. Bob
keeps his place even though he was partially filled; he's still the earliest order at that
price.

---

### Scenario 6: A sell sweeping bids
E sells 250 @ 14.50 and looks at bids, highest first:
1. A 100 @ 15.00 (earlier at 15.00). 15.00 >= 14.50, cross. Fill **100 @ 15.00**. 150 left.
2. B 100 @ 15.00. Cross. Fill **100 @ 15.00**. 50 left.
3. C 300 @ 14.00. Is 14.00 >= 14.50? **No.** C only wants to pay 14; E won't sell below 14.50. Stop.
4. E's 50 **rests as an ask @ 14.50**.

**Trades:** A/E 100 @ 15.00 · B/E 100 @ 15.00 (E sells at a *higher* price than it asked for)
```
BIDS                  ASKS
C 300 @ 14.00         E  50 @ 14.50
                      D 100 @ 16.00
```
Sanity: 14.00 < 14.50. ✓

---

### Scenario 7: Full sequence
| Step | Trades | Book after (BIDS / ASKS) |
|---|---|---|
| 1. A buy 100 @ 10.00 | none | B: A 100@10.00 / A: — |
| 2. B buy 50 @ 10.10 | none | B: **B 50@10.10**, A 100@10.00 / A: — |
| 3. C sell 80 @ 10.20 | none (best bid 10.10 < 10.20) | B: B 50@10.10, A 100@10.00 / A: C 80@10.20 |
| 4. D sell 120 @ 10.00 | **B/D 50 @ 10.10**, then **A/D 70 @ 10.00** | B: A 30@10.00 / A: C 80@10.20 |
| 5. E buy 100 @ 10.30 | **E/C 80 @ 10.20** | B: E 20@10.30, A 30@10.00 / A: — |
| 6. F sell 30 @ 10.30 | **E/F 20 @ 10.30** (next bid 10.00 < 10.30, stop) | B: A 30@10.00 / A: F 10@10.30 |

Notes:
- Step 4: D hits the **higher** bid (B @ 10.10) first even though A arrived earlier. Price
  beats time. D sold 50 @ 10.10 and 70 @ 10.00, two different prices from one order.
- Step 5: E's leftover 20 rests @ 10.30, its own limit.

**All trades:** 50 @ 10.10 · 70 @ 10.00 · 80 @ 10.20 · 20 @ 10.30. **Total volume = 220.**

Final book: bids `A 30 @ 10.00`, asks `F 10 @ 10.30`. Spread 0.30.

---

### Scenario 8: Cancels
1. Anne's order is removed. Book: asks `Bob 100 @ 16.00`.
2. You buy 100 @ 16.00, so you **trade with Bob, 100 @ 16.00**. Book empty.
3. *(Beyond the primer, common exchange practice.)* **Reducing size keeps priority;
   increasing size loses it** (treated like a new order and goes to the back). Changing the
   price always loses priority. Reasoning out loud: if increasing size kept your place, you
   could rest a tiny order early and grow it later to jump the queue. That's unfair to
   everyone who arrived in between.
4. **It's a race.** The exchange processes messages one at a time, in the order it received
   them. If your buy is processed first, you trade with Anne and her cancel gets rejected
   ("too late to cancel"). If her cancel is processed first, you trade with Bob. Either way
   the outcome is deterministic once the order is fixed. This is why exchanges **sequence**
   every message.

---

### Scenario 9: Bigger than the whole other side
- C/A **100 @ 16.00**, C/B **100 @ 17.00**. Asks now empty. Loop stops because the opposite
  side is empty.
- C's leftover **300 rests as a bid @ 20.00**.
```
BIDS                  ASKS
C 300 @ 20.00         (empty)
```
- Nothing is wrong. A one-sided book is valid; there's just no best ask and no spread. In
  code, make sure "best ask" on an empty side doesn't crash (return None).
- Out loud: "C paid two different prices and is now the best bid by a mile. If that was a
  fat-finger, a real exchange's **price band / risk check** would usually reject a $20 bid
  when the market is $16–17." That's a nice TDOE-flavored point.

---

### Scenario 10: Work backward
- Trades are at the **resting bids'** prices: 15.00 first, then 14.00. A sell hits the highest bid
  first, so the bids before were at least `100 @ 15.00` and `50 @ 14.00` (maybe more at
  lower prices).
- **Price:** it traded at 14.00, so the sell's limit was **≤ 14.00**.
- **Quantity: ≥ 150.**
  - If exactly 150, it was fully filled and nothing rests.
  - If more than 150, matching stopped because no more bids crossed. Either the bid side ran
    out, or the next bid was below the sell's limit. The leftover **rests as an ask** at the
    sell's limit (≤ 14.00).
- This is exactly the primer's "Multiple Executions and Partial Executions" example: Bob sold
  200 @ 14.00 and 50 rested.

---

## Concept check answers

1. **Bid** = order to buy, **offer/ask** = order to sell.
2. **$10 or lower.** A bid is a *maximum* price.
3. **No.** Any incoming order that would cross trades immediately until it no longer
   crosses, so whatever rests is always below (bids) or above (asks) the other side.
4. **The earlier one.** Time priority.
5. **The $15.50 offer.** Better price wins, regardless of time.
6. Each resting order has its own price. A large order fills against several in turn, and
   each trade uses that resting order's price.
7. **No.** It's still the oldest order at that price.
8. Best ask − best bid. A wide spread means less liquidity or more uncertainty; it's more
   expensive to trade immediately.
9. A crossing order trades **instantly** on arrival. Only the *unfilled leftover* (if any)
   ever sits on the book.
10. To **get a better price**: you might buy cheaper if a seller comes to you, at the
    risk of never getting filled. Paying the ask = certainty now; resting a bid = better
    price, maybe.
