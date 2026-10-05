# Design a Stock Exchange / Order Book System

Reported as "stock exchange system design whiteboarding" and "a long case study of designing
order books". It builds directly on the primer.

**Time: 45 min.** Use the 6-step framework from `00_how_to_whiteboard.md`.

---

## The prompt
> "Design a simple stock exchange. Participants should be able to send orders, cancel them,
> and find out when they trade. Other people should be able to see what the market looks like."

## Follow-ups the interviewer will likely push (one at a time)
1. Walk me through exactly what happens when an order arrives.
2. What data structure holds the book? (You already built one.)
3. How do you guarantee price-time priority is **fair**, i.e. who was "first"?
4. A participant sends a cancel at the same moment someone trades against their order. What
   happens?
5. The matching engine crashes mid-day. How do you recover the book?
6. Someone fat-fingers a buy for 1,000,000 shares at 10x the market price. What stops it?
7. How do you support 5,000 symbols?
8. How does a market-data subscriber know they haven't missed an update?

Try it on a whiteboard (or paper) before scrolling.

<br><br><br><br><br><br><br><br><br><br><br><br>

---
---

## MODEL ANSWER

### 1. Clarify
- Stocks only, limit orders only (buy/sell, price, qty), plus cancel. Price-time priority,
  trades at the resting price, per the primer.
- Outputs: to the participant, acks/rejects/fills. To the public, market data.
- Priorities: **correctness and fairness** first, then speed.

### 2. The boxes
```
 Participants
     │  new order / cancel
     ▼
┌───────────┐   reject   ┌──────────────┐
│  Gateway  │◄──────────│  Risk checks  │
│ (validate,│──────────►│ (size, price  │
│  ack)     │            │  band, limits)│
└───────────┘            └──────┬───────┘
                                ▼
                         ┌─────────────┐      ┌────────────────┐
                         │  Sequencer  │─────►│  Journal / log │ (every input, in order)
                         │ (seq # each)│      └────────────────┘
                         └──────┬──────┘
                                ▼
                     ┌────────────────────┐
                     │  Matching engine   │  one order book per symbol
                     │ (price-time loop)  │
                     └───┬───────────┬────┘
                         │           │
            fills/acks   ▼           ▼   book updates + trades
                ┌──────────────┐  ┌──────────────────┐
                │ Exec reports │  │ Market data feed │ ──► public subscribers
                │ (+ drop copy)│  │ (seq numbered)   │
                └──────┬───────┘  └──────────────────┘
                       ▼
                 Participants, clearing/settlement
```

### 3. Walk one order through
1. Anne sends `BUY 100 AAPL @ 16.00`.
2. **Gateway** checks it's well-formed (known symbol, qty > 0, price > 0, valid side), gives
   it an order ID.
3. **Risk checks:** is the size under the max? Is the price within, say, 10% of the
   last trade? Rejects go straight back to Anne with a reason.
4. **Sequencer** stamps it with sequence #1,042 and writes it to the **journal** *before*
   it's processed.
5. **Matching engine** runs the primer's loop on the AAPL book: match against asks
   ≤ 16.00, lowest first, earliest first, at the resting price, and rest any leftover.
6. Outputs:
   - Anne gets an **ack**, then **fill** messages (qty, price) for each trade.
   - The seller gets their fill too.
   - **Market data** publishes the trade(s) and the new top of book, each with a sequence
     number.

### 4. Data
- **Order:** id, participant, symbol, side, price, qty remaining, original qty, seq/time.
- **Book (per symbol):** bids and asks, each sorted best-first. Better: a map
  `price → FIFO queue of orders` plus a sorted set of prices. Also `order_id → order`
  for fast cancels.
- **Trade:** trade id, symbol, price, qty, buy order id, sell order id, seq/time.
- **Prices as integers** (cents/ticks), never floats.

### 5. What goes wrong (the important part)
| Question | Answer |
|---|---|
| **Fairness: who's first?** | The **sequencer**. Messages are processed one at a time in sequence-number order. "Time priority" means sequence order, not wall-clock time. |
| **Cancel vs trade race** | Whichever the sequencer processed first wins. If the trade was first, the cancel gets "too late to cancel" for the filled part. Deterministic and explainable. |
| **Engine crashes** | The engine is **deterministic**, and every input was journaled before processing. Start a fresh engine and **replay the journal** in order to rebuild the exact same book. Better still, run a hot **standby** that processes the same stream and can take over. |
| **Fat finger** | Pre-trade **risk checks**: max order size, **price bands** (reject prices too far from the last trade), per-participant limits. Plus **circuit breakers / trading halts** if the price moves too far too fast. |
| **Lost market-data messages** | Each message has a sequence number. If a subscriber sees #10 then #12, it knows it missed #11 and asks for a **retransmit** or a fresh **snapshot** of the book. |
| **Duplicate order sent** | Participant includes a client order ID; the gateway rejects a reused one. |
| **Gateway disconnects** | Common policy: **cancel on disconnect**, so nobody is left with live orders they can't manage. |
| **How would ops know?** | Monitor: message rates, latency, rejects per participant, gaps, engine heartbeat. Alert on anything unusual. |

### 6. Scale
- **5,000 symbols:** each symbol's book is independent, so **split symbols across engines**
  (e.g., A–F on engine 1). The gateway routes by symbol. No cross-symbol coordination needed.
- Most activity is near the top of book, so the book data structure stays fast in practice.

### If you only remember 5 things
1. Gateway → risk → **sequencer + journal** → matching engine → fills + market data.
2. The sequencer defines "first", and that's what makes it fair.
3. Deterministic engine + journal = **replay to recover**.
4. Sequence numbers everywhere = **detect gaps and duplicates**.
5. Risk checks and halts stop fat fingers.
