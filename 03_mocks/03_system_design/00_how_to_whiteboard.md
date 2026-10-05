# How to Do a TDOE Whiteboard Design Round

This **is not** a FAANG "design Twitter for a billion users" round. For an intern TDOE, they
want to see that you can:
- break a trading system into sensible pieces,
- follow **one order or one trade** through it step by step,
- think about **what goes wrong** (missing, duplicated, out of order, wrong data, crashes),
- ask good questions instead of assuming.

The **"what goes wrong"** part is the TDOE part. TDOEs are the people who get called when the
trading system misbehaves. Lean into it.

---

## The 6-step framework (use it every time)

1. **Clarify (2–3 min).** Who uses it? What goes in, what comes out? How many symbols /
   messages, roughly? What matters most: speed, correctness, fairness? Say your assumptions
   out loud.
2. **Draw the boxes (5 min).** 4–6 boxes with arrows. Name each one by its job.
3. **Walk one example through (5 min).** "Anne sends a buy order. It goes here, then here..."
   This is where you show you understand it.
4. **Data (5 min).** What does each message contain? What does each box store?
5. **What goes wrong (10 min).** For each arrow: what if the message is lost? Duplicated?
   Late? Wrong? What if a box crashes? How would you **notice**? (Monitoring, alerts,
   reconciliation.)
6. **Scale and extras (if time).** More symbols, more traffic, new features.

**Keep talking and keep drawing.** Silence at a whiteboard reads badly. If you're thinking,
say what you're thinking about.

---

## The vocabulary (just enough to sound fluent)

| Term | Plain meaning |
|---|---|
| **Gateway / order entry** | The front door. Receives orders, checks they're well-formed, tells the sender "got it" (ack) or "rejected". |
| **Pre-trade risk checks** | Sanity checks before an order reaches the market: max order size, price far from the market ("fat finger"), position limits. |
| **Sequencer** | Puts every incoming message into **one definite order** and stamps it with a sequence number. This is what "time priority" really means. |
| **Matching engine** | The order book plus the matching loop from `01_order_book`. One book per symbol. |
| **Execution report / fill** | Message telling a participant their order traded (how much, what price). |
| **Market data feed** | Public broadcast of the book's state and trades (top of book, depth, last trade). |
| **Drop copy** | A second, independent copy of your fills sent to you, used to double-check (reconcile). |
| **Sequence number** | An increasing number on every message so the receiver can detect **gaps** (missing) and **duplicates**. |
| **Idempotent** | Processing the same message twice has the same effect as processing it once (e.g., dedupe by trade ID). |
| **Audit log / journal** | An append-only record of every input, in order. Lets you **replay** to rebuild state after a crash and explain any outcome later. |
| **Reconciliation** | Comparing two independent records (ours vs exchange's / clearing's) and investigating differences. |
| **Bust / correction** | The exchange cancels or amends a trade after the fact. |

---

## Phrases that land well
- "Before I draw anything, can I check what we're optimizing for?"
- "Let me follow a single order through this end to end."
- "What happens if this arrow drops a message? We'd want sequence numbers so the receiver
  notices the gap and asks for a resend."
- "I'd want the matching engine to be **deterministic**: same inputs in the same order give
  the same book. Then if it crashes, we replay the log and get exactly the same state."
- "How would an operator *know* this broke? I'd add an alert on X."
- "I'm going to keep this simple first and then we can add the harder parts."

## Traps to avoid
- Jumping straight into databases, Kubernetes, microservices. Stay at the level of "what
  are the pieces and how do messages move".
- Designing in silence for 5 minutes.
- Ignoring failure. A design with no "what if it breaks" section misses the point of TDOE.
- Pretending to know something. "I'm not sure how real exchanges do X, but I'd guess Y
  because Z" is a great answer.
