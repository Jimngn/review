# The Order Book Primer on One Page

Everything here comes from Jane Street's `Resource/Order_20Book_20Basics_20Primer.pdf`.
Anything marked **(beyond the primer)** is common real-world knowledge. Say it as "usually",
not as a fact about their system.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Bid** | An order to **buy**. "Bid 100 @ $10" = willing to buy 100 at $10 *or lower*. |
| **Offer / Ask** | An order to **sell**. "Offer 100 @ $10" = willing to sell 100 at $10 *or higher*. |
| **Order book** | All the **unmatched** bids and offers for one stock, kept by the exchange. |
| **Resting order** | An order already sitting on the book. |
| **Incoming / aggressive order** | The new order that just arrived and may trade with resting orders. |
| **Cross** | Bid price >= ask price. They pair and trade. |
| **Trade / execution / fill** | A matched buy and sell. |
| **Partial execution** | An order traded some of its quantity. The rest is still live. |
| **Best bid / best ask** | Highest bid / lowest ask. Together: "top of book" or "the inside". |
| **Spread** | Best ask − best bid. |
| **Price level** | All resting orders on one side at the same price. |

---

## The 6 rules

1. **Trade condition:** a bid and an offer trade if `bid_price >= ask_price`. **Equal counts.**
2. **Execution price = the resting order's price.** The incoming order gets whatever price
   was already on the book, even if it was willing to pay more or sell for less.
3. **Price priority:** the incoming order matches the *most competitive* resting order first.
   - An incoming **buy** hits the **lowest** ask first.
   - An incoming **sell** hits the **highest** bid first.
4. **Time priority:** among resting orders at the **same price**, the **earliest** goes first.
   Time only breaks ties; it never beats a better price.
5. **Fill quantity** for each match = `min(incoming remaining, resting remaining)`. Keep
   matching against the next-best resting order until the incoming order is fully filled
   **or** the next-best resting price no longer crosses.
6. **Leftover rests:** if the incoming order still has quantity left, it goes onto the book
   **at its own limit price**, behind any earlier orders at that price.

**Consequence:** after an order finishes matching, the book is never crossed. The best bid
is always strictly below the best ask. If you ever draw a crossed book after processing an
order, you made a mistake.

---

## The matching loop in plain English

```
when an order arrives:
    look at the opposite side of the book, best price first
    while my order still has quantity AND the opposite side is not empty:
        best = best resting order on the opposite side
        if best's price doesn't cross my price: stop
        fill = smaller of (my remaining qty, best's remaining qty)
        record a trade: fill shares at BEST'S price
        subtract fill from both orders
        if best is now empty, remove it from the book
    if my order still has quantity left:
        put it on my side of the book, sorted by price, behind earlier orders at that price
```

Memorize this. Every scenario, the build exercise, and the "design an exchange" question all
come back to it.

---

## The traps they test

| Trap | Wrong | Right |
|---|---|---|
| **Execution price** | Trade at the incoming price | Trade at the **resting** price |
| **Equal prices** | "15 and 15 don't cross, so no trade" | **Equal trades** |
| **Leftover** | Leftover disappears | Leftover **rests at its own limit price** |
| **Sweep stops** | Keep matching through worse prices | **Stop** as soon as the next price doesn't cross |
| **Time vs price** | Earlier order wins | **Price first**, time only at the same price |
| **Sort direction** | Both sides sorted the same way | Bids **high to low**, asks **low to high** |
| **Partial resting fill** | Partially filled resting order goes to the back | It **keeps its place** (still the oldest) |
| **Multiple trades** | One order makes one trade | One order can make **many** trades, each at a different price |

---

## Why does the trade happen at the resting price? (they may ask)

- The resting order was there first and **publicly showed** that price. It set the market.
- The incoming order is getting **at least as good** a price as it asked for. A buyer
  willing to pay $18 who gets filled at $16 is happy. This is called **price improvement**.
- It gives a clear, deterministic rule. Every participant can predict the outcome.

---

## Reading the primer's tables

The primer shows the book as one table with bids on the left and asks on the right. **Each
row pairs up the next-best bid with the next-best ask; the two halves are independent.**
Row 1 is top of book.

```
Bid Qty | Bid Px || Ask Px | Ask Qty
   100  | 15.00  || 16.00  |  100      ← best bid 15.00, best ask 16.00, spread 1.00
    50  | 14.00  || 17.00  |   50
```

In practice, write orders with an **ID, trader, and arrival order** so you can track time
priority:

```
BIDS (high → low)            ASKS (low → high)
#1 A  100 @ 15.00            #2 B  100 @ 16.00
#3 C   50 @ 14.00            #4 D   50 @ 17.00
```

---

## Out-loud lines worth having ready

- "Before I trace this, let me confirm: trades execute at the resting order's price, and equal
  prices count as a cross?"
- "The incoming order is a buy, so I'm looking at the ask side starting from the lowest price."
- "That fill used up the resting order, so it comes off the book and I move to the next one."
- "The next ask is $17, which is above my $16.50 limit, so matching stops and the remaining 100
  rest on the bid side at $16.50."
- "Sanity check: best bid 16.50 < best ask 17.00, so the book isn't crossed. Good."
