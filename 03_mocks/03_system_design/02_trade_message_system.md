# Design a Trade Message System

Reported directly: "Design a trade message system". This is very TDOE: once a trade
happens, many systems (positions, P&L, risk, booking/clearing) need to hear about it
**exactly once, correctly, in order**. When they don't, a TDOE gets the call.

**Time: 40 min.** Then do `04_trade_message_code.md`, which has you write the code for
this design (dedupe, gap detection, busts).

---

## The prompt
> "When we trade on an exchange, the exchange sends us a message for each fill. Design the
> system that gets those trade messages to everyone inside the firm who needs them."

## Follow-ups (one at a time)
1. What fields does a trade message need? Why each one?
2. Who are the consumers and what does each one do with a trade?
3. A message gets lost. How does anyone notice? How do you recover?
4. A message arrives **twice**. What breaks, and how do you prevent it?
5. The exchange **busts** (cancels) a trade an hour later. How does that flow through?
6. The positions service crashes and restarts. How does it get back to the right state?
7. At end of day, how do you **prove** your records are right?

<br><br><br><br><br><br><br><br><br><br><br><br>

---
---

## MODEL ANSWER

### 1. Clarify
- Source: exchange fill messages (maybe several exchanges). Consumers: positions, P&L,
  risk, trader blotter/UI, booking/clearing, ops dashboards.
- Priorities: **no lost trades, no double-counted trades**, then low latency. A missed or
  duplicated trade means a wrong position, which means wrong risk.

### 2. The message
| Field | Why |
|---|---|
| `trade_id` (unique, from exchange) | Identity: dedupe, corrections, reconciliation |
| `order_id` | Links the fill back to our order |
| `symbol` | What |
| `side` | BUY / SELL (sign of the position change) |
| `qty` | How much |
| `price` (integer cents/ticks) | At what price, with no float errors |
| `exec_time` | When it happened at the exchange |
| `account` / `trader` / `strategy` | Whose position it is |
| `exchange` | Where (and IDs are only unique per exchange) |
| `seq_num` | Position in the stream: detects gaps and duplicates |
| `msg_type` | NEW / CORRECT / BUST |
| `ref_trade_id` | For corrections/busts: which trade is being changed |

### 3. The boxes
```
 Exchange A ─┐                                        ┌──► Positions service
 Exchange B ─┼─► Feed handlers ─► Normalizer ─► Trade log / bus ─┼──► P&L
 Exchange C ─┘   (one per exch,   (common       (append-only,     ├──► Risk
                  track seq #s)    format)       seq numbered,    ├──► Trader UI / blotter
                                                 durable)         └──► Booking / clearing
                                                                      
                 Exchange drop copy / clearing file ─────────► End-of-day reconciliation
```
- **Feed handler:** speaks each exchange's protocol and tracks that exchange's sequence numbers.
- **Normalizer:** converts every exchange's format into **one internal format**, so
  consumers don't care where a trade came from.
- **Trade log / bus:** an **append-only, durable, ordered** log. Every consumer reads it in
  order and remembers "I've processed up to seq N".

### 4. Walk one trade through
Exchange sends fill `seq 501: trade X123, BUY 100 AAPL @ 150.00`. The feed handler sees
seq 501 follows 500 (no gap) and passes it on. The normalizer converts it, and it's appended
to the log as internal seq 9,001. Positions adds +100 AAPL to the account, P&L marks it,
risk re-checks limits, the blotter shows it. Each consumer records "done through 9,001".

### 5. What goes wrong
| Problem | Detect | Handle |
|---|---|---|
| **Lost message** | Sequence gap (500 → 502) | Ask the exchange to **retransmit** 501. Don't process 502 onward for positions until the gap is filled, or flag the gap loudly. |
| **Duplicate** | `trade_id` (or seq) already seen | Consumers are **idempotent**: keep a set of processed trade IDs and ignore repeats. Delivery can then safely be "at least once". |
| **Out of order** | seq lower than expected | Buffer and reorder by seq, or rely on the ordered log. |
| **Bust / correction** | `msg_type` = BUST/CORRECT with `ref_trade_id` | **Never edit history.** Append a new message that reverses or amends the original. Positions apply the reversal. You keep a full audit trail. |
| **Consumer crashes** | Heartbeat stops / lag grows | On restart, **replay the log from its last checkpoint** (or from start of day). Idempotency makes replaying overlapping messages safe. |
| **Malformed message** | Validation fails | Don't drop it silently and don't crash. Put it in an **error queue**, alert, have a human look. |
| **Slow consumer** | Lag metric (log head seq − consumer seq) | Alert. The log buffers it so nothing is lost. |

### 6. End-of-day proof: reconciliation
Compare our trade log against an **independent** source: the exchange's **drop copy** or
the **clearing firm's** file. Match by `trade_id` (the `reconcile` function from
`02_coding` problem 7). Report missing on either side and mismatched qty/price/side. Every
break gets investigated before the next trading day.

### If you only remember 5 things
1. **Unique trade ID + sequence number** on every message.
2. **Gaps** → retransmit. **Duplicates** → idempotent consumers dedupe by trade ID.
3. **Append-only log**: consumers replay from a checkpoint after a crash.
4. **Corrections are new messages**, never edits.
5. **Reconcile** against an independent source every day.
