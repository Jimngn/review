# Answer Key — Mock 11 (Trading System Design)

There is no single right design. You are scored on **whether you drove the conversation
through a sensible structure, named trade-offs instead of asserting choices, and knew which
part was genuinely hard.** What follows is the material to have loaded, not a script.

---

## The opening, verbatim
Use something like this every time — it buys you ten minutes of thinking and immediately
reads as senior:

> *"Before I draw anything: who's using this, what's the scale, and what's the thing it
> absolutely cannot get wrong? Let me also say what I'm going to leave out, so you can stop
> me if I'm scoping it wrong."*

Then **actually state exclusions**: "I'll assume a single data centre, I won't design
authentication, and I'll treat clearing as a downstream consumer." Interviewers almost always
say "sounds good" — and now you can't be penalized for omitting them.

---

## Case A — exchange / order book

### The shape to draw
```
participants
    |
[ order gateways ]        validation, auth, pre-trade risk
    |
[ sequencer ]             assigns a single global order; THE critical component
    |
[ matching engine ]       sharded by symbol, single-threaded per book
    |         \
    |          \--> [ market data publisher ] --> subscribers
    |
[ message log ]           durable, replayable, the source of truth
    |
[ drop copy / clearing / surveillance ]
```

### The five things that earn the round

**1. Single-threaded per book, sharded by symbol.** Candidates reach for threads to go
faster; real exchanges deliberately do the opposite. Say why: matching is inherently
sequential (the result depends on the exact order of arrival), so parallelism *within* a book
would make outcomes non-deterministic and unauditable. You scale by **running many books in
parallel**, because no order ever touches two symbols. That's near-linear scaling with zero
coordination.

**2. The log is the source of truth; state is derived.** Persist the *input messages* in
sequence, not the book state. Recovery = replay the log. This gives you crash recovery,
audit, deterministic testing, and the ability to answer "what did the book look like at
10:31:02?" — four hard problems solved by one decision. **This is the single highest-value
idea in the whole round; make sure you say it.**

**3. Determinism.** Same input sequence → same output, always. Which means: no wall-clock
reads in matching logic, no hash iteration order dependence, no randomness, no floating point
where integers will do. If asked "how do you test this?", the answer falls out: **capture a
day of production input and replay it against the new build; the output must be byte-identical.**

**4. Sequence numbers everywhere, on market data especially.** Every published update carries
a monotonic sequence number. A client detecting a gap knows it missed something and requests
a snapshot. Without this, a dropped packet silently corrupts a consumer's book forever —
which is exactly the kind of production incident a TDOE handles.

**5. Pre-trade risk sits in the gateway, before the engine.** The matching engine's hot path
must stay minimal. Credit limits, fat-finger checks, and max order size belong upstream.

### Answers to the expected follow-ups

**"Engine crashes mid-day."** Replay the log into a standby. Discuss the real decision:
*hot standby* consuming the same sequenced input in parallel (fast failover, more hardware)
vs *cold restart* from the log (simpler, slower). Note what's genuinely hard — not restoring
the book, which is mechanical, but **deciding what happened to in-flight orders** at the
moment of the crash, and making sure the standby doesn't double-publish trades the primary
already sent.

**"How do two participants see the same market data?"** They consume the same sequenced
feed. Fairness is a real design concern — equal-length cables, multicast so one publish
reaches everyone simultaneously rather than a serialized loop that favours whoever is first
in the list.

**"A participant claims they sent an order you have no record of."** This is a **TDOE
question dressed as design** — answer it operationally: check the gateway's receive log
first, since the question is whether it ever arrived; compare sequence numbers on their
session; look for a gap or a session disconnect. The reason you can answer at all is that
you logged inputs at the boundary. Tie it back to decision 2.

---

## Case B — trade message system

### The sentence that carries the round
> *"I'd do at-least-once delivery with idempotent consumers keyed on trade ID, rather than
> trying to build exactly-once. Exactly-once across a network is extremely expensive and
> usually turns into at-least-once plus deduplication anyway — so I'd put the dedupe where
> it's cheap and visible."*

### Points worth making
- **Partition for ordering.** Global total ordering caps throughput at one partition. Order
  *within* a symbol or account is nearly always what's actually needed. Ask which.
- **Consumers own their offset.** That's what makes replay and catch-up possible, and it
  decouples a slow consumer from a fast one.
- **Schema evolution is a real risk over years.** Additive-only fields, versioned schemas,
  consumers ignore unknown fields. A system that can't add a field without a coordinated
  firm-wide deploy is broken.
- **Poison messages.** One malformed message must not crash every consumer in a retry loop
  forever. Dead-letter queue, alert, move on.
- **Backpressure vs dropping.** For trades you must never drop — buffer, spill to disk, or
  slow the producer. Contrast with market data, where dropping stale quotes is *correct*.
  Knowing where each applies is the sophisticated answer.

---

## Case C — position and P&L

- **Trade log is truth; position is a materialized view.** Same idea as Case A.
- **Incremental + periodic full recompute.** Name both and why: incremental is O(1) per trade
  but drifts and can't be audited; full recompute is correct but O(n). Running both and
  alerting on divergence is how real systems catch bugs — and **that alert is a TDOE's
  morning.**
- **Amendments and busts.** Never mutate history. Append a signed correcting entry, or replay
  the log with the bad trade removed. If you mutate, you lose the audit trail and can never
  explain yesterday's number.
- **Stale or missing marks.** Show the position as unmarked rather than defaulting to zero,
  which would silently report a total loss on something you still hold. Flag the staleness
  with a timestamp.
- **Reconciliation** against the broker/clearer at end of day, with a break report listing
  differences. Mentioning this unprompted is strongly role-aware — resolving breaks is
  literally part of the job.

---

## Case D — market data

- **Conflation is valid for quotes, invalid for trades.** A quote is a *state* — only the
  latest matters, so dropping intermediates is lossless for the consumer's purpose. A trade
  is an *event* — every one is a fact that happened, and dropping one corrupts volume,
  VWAP, and P&L. **This distinction is the best single answer available in Case D.**
- Normalize at the edge: one adapter per exchange, one internal format downstream.
- A/B feed arbitration: take the first copy of each sequence number, discard the duplicate.
- Snapshot + incremental: a late joiner gets a snapshot then applies increments from that
  sequence number forward.

---

## Scoring yourself
- [ ] Spent the first 5–10 minutes on requirements and scope, not boxes
- [ ] Stated explicit exclusions and got agreement
- [ ] Said "the log is the source of truth, state is derived" in Cases A or C
- [ ] Named at least three trade-offs as trade-offs ("X buys us Y at the cost of Z")
- [ ] Identified failure modes without being asked
- [ ] Connected at least one answer to the operational reality of the TDOE role
- [ ] Said "I don't know, here's how I'd find out" instead of bluffing, at least once if true

## The three ways people fail this round
1. **Drawing before scoping.** Ten minutes of boxes for a system nobody specified.
2. **Asserting instead of trading off.** "I'd use Kafka" is not a design. *Why*, and what
   does it cost you?
3. **No failure modes.** For a TDOE role especially, a design with no answer to "what breaks
   and how do you find out at 9:31am" is incomplete regardless of how elegant the happy path is.
