# Mock 11 — Trading System Design (whiteboard, 45–60 min each)

**This is the round I most under-weighted, and your Glassdoor reports make it unmissable.**
Five separate accounts describe it:

> "Stock Exchange system design white boarding" · "2 trading system design, 1 coding" ·
> "design of trading systems and infrastructure — at a whiteboard" · "Design a trade message
> system" · "goes into a long case study of designing order books"

For an onsite with three technical rounds, **two of them being design** is the single most
likely shape. Weight your prep accordingly: this is probably more of your day than coding is.

## What's different about this round
No code. No interpreter. A whiteboard or a shared blank doc. You are judged on **structure
and trade-offs**, not syntax. The failure mode is jumping straight to boxes and arrows
before establishing what the system is for.

**Use this frame every time, out loud, in this order:**
1. **Requirements** — what must it do, who uses it, what's the scale?
2. **Scope** — say what you're explicitly leaving out, and get agreement.
3. **Data model** — the two or three core entities and their fields.
4. **Components** — boxes and the flow between them. Draw it.
5. **The hard part** — pick the one genuinely difficult thing and go deep.
6. **Failure modes** — what breaks, and how do you know? (For TDOE this is the whole job.)
7. **Scale** — what falls over first at 10x, and what do you change?

Spend the first 5–10 minutes on steps 1–2. Candidates who skip them design the wrong system
confidently, which is worse than designing nothing.

---

## Case A — Design an exchange / order book system
> "Design the system that runs a stock exchange. Participants send orders in, trades come
> out."

Run the frame. Questions you should raise yourself before drawing anything:
- How many symbols? How many orders per second? How many participants?
- Is this one matching engine or many? What's the partitioning key?
- Does it need to be deterministic and replayable? (For an exchange: **yes**, and this
  drives most of the design.)
- What's the latency target — microseconds, or "fast enough for a human"?

Then be ready to go deep on, in roughly this order of likelihood:
- **The matching engine core** — this is where your Mock 5 work pays off. Price levels, FIFO
  queues, O(1) cancel. Draw the data structure.
- **Partitioning by symbol.** Each symbol's book is independent, so you shard by symbol and
  get near-linear scaling. Say *why* this works: no order ever touches two books.
- **Sequencing and determinism.** A single sequencer assigns a monotonic order to incoming
  messages; every downstream component applies them in that order. This is how you get
  replayability, audit, and recovery — and it's why exchanges are famously **single-threaded
  per book** rather than cleverly parallel.
- **Market data out** — the feed publishing trades and book updates. Snapshot plus
  incremental updates, with sequence numbers so a client can detect a gap and request a
  re-snapshot.
- **Gateways** — order entry, validation, authentication, risk checks *before* the engine.
- **Persistence and recovery** — write the input message log, not the state. Rebuild state by
  replaying. Say why: the log is the source of truth and makes the whole system auditable.
- **Risk/credit checks** — pre-trade limits per participant.

Follow-ups to expect:
- "What happens if the matching engine crashes mid-day?"
- "How do you make sure two participants see the same market data?"
- "How do you test this?"
- "A participant claims they sent an order you have no record of. How do you resolve it?"

---

## Case B — Design a trade message system
> "Design a system for distributing trade messages across the firm."

This is a **messaging/pub-sub** problem wearing trading clothes. The core tension: lots of
consumers (risk, P&L, clearing, compliance, reporting) with different needs for the same
stream.

Raise these yourself:
- **Delivery guarantees** — at-most-once, at-least-once, or exactly-once? Say plainly that
  exactly-once is very expensive and usually approximated with **at-least-once delivery plus
  idempotent consumers keyed on a trade ID**. That sentence alone is most of the answer.
- **Ordering** — global order, or per-symbol/per-account order? Global ordering kills
  throughput; partitioned ordering is the usual answer.
- **Replay** — can a consumer that was down for an hour catch up? (It must.) That means the
  log is retained and consumers track their own offset.
- **Schema evolution** — trade messages gain fields over years. How do old consumers survive
  a new field? (Versioned schemas, additive-only changes.)
- **Fan-out** — slow consumers must not block fast ones.
- **Audit** — regulators will ask what was sent and when.

Draw: producers → sequenced durable log → topics/partitions → consumer groups, each with its
own offset. Then name the failure modes: duplicate delivery, out-of-order within a partition,
consumer lag, and the poison message that crashes a consumer on every retry.

---

## Case C — Design trading infrastructure / position & P&L system
> "The desk needs to know its position and P&L in real time. Design that."

Ties directly to Mock 8. Key points to surface:
- **Source of truth is the trade log**, not the computed position. Positions are a *view*.
- **Incremental updates** for speed, with **periodic recomputation from the log** to catch
  drift. Say why you want both: incremental is fast but unauditable and can silently skew;
  full recompute is correct but slow.
- **Marks** — you need a price source, and it can go stale or be wrong. What do you show when
  a mark is missing? (Not zero.)
- **End-of-day reconciliation** against the clearing broker's records — this is a real TDOE
  responsibility and mentioning it is a strong, role-aware signal.
- **Corrections and busted trades.** A trade can be cancelled or amended *after the fact*.
  If your position is a running incremental total, how do you un-apply it? (Replay from the
  log, or store signed adjustment entries — never mutate history.)

---

## Case D — Design a market data system
> "Design the system that takes in market data from several exchanges and makes it available
> to the desk."

- Normalization: every exchange's format is different; one internal format.
- Conflation: when updates arrive faster than a consumer can handle, you drop intermediate
  states and send the latest — valid for quotes, **not** for trades. Explain the difference.
- Gap detection via sequence numbers; recovery via snapshot.
- Latency vs completeness trade-off.
- A/B feed arbitration: exchanges publish two identical feeds; take whichever packet arrives
  first, deduplicate by sequence number.

---

## Practice protocol
Do each case on an actual whiteboard or blank page, standing up, talking out loud, for 45
minutes. **Then** read the key. Do Case A twice — once cold, once a week later.
