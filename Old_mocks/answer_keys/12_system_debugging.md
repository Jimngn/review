# Answer Key — Mock 12 (System Debugging)

The grading is on **method, not the specific root cause**. If you narrow systematically and
say what evidence would distinguish your hypotheses, you pass even if you guess the cause
wrong. If you leap to a cause without a way to test it, you fail even if you happen to be right.

---

## Scenario 1 — position break (long 5,000 vs 4,800)

**First move, out loud, before any hypothesis:**
> *"200 shares. Before I guess why — is that one trade or many? And was the position
> reconciled correctly at yesterday's close?"*

That second question is the highest-value one in the scenario, because it **bisects time**:
if yesterday reconciled clean, the break was created today and you only have to examine
today's activity. If it didn't, you're chasing something older and today's trades are a
distraction.

**Hypotheses, roughly in order of real-world likelihood:**
1. **A trade we have and they don't** — it never reached the broker, or was rejected and we
   didn't process the rejection. (Our number too high: 5,000 > 4,800. ✓ consistent.)
2. **A trade booked twice on our side** — at-least-once delivery without dedupe.
3. **A corporate action** — split, dividend in shares, symbol change — processed by one side
   and not the other. Mentioning this marks you as someone who's seen real breaks.
4. **Timing/cut-off**: a trade that we count in today and they count in tomorrow. Very common
   and completely benign.
5. **Allocation**: the trade was done in one account and allocated to another; we're looking
   at different account groupings.
6. A **busted trade** the exchange cancelled that we never un-booked.

**The test that separates them fastest:** get the broker's trade-level detail and diff it
against ours on trade ID. A 200-share single difference points at (1) or (6); 200 made of
many small differences points at (4) or (5). **Always say the diff should be at trade level,
not position level** — comparing totals tells you there's a problem, comparing trades tells
you which one.

**"The trader is about to do a big trade. What do you tell him?"**
Do not say "wait while I investigate." Say the two numbers, the size of the uncertainty, and
which one you'd act on:
> *"We're long somewhere between 4,800 and 5,000 — the uncertainty is 200 shares. If you're
> sizing something where 200 shares matters, use 4,800 and assume the worst case until I come
> back. I'll have an answer in X minutes."*
Quantifying the uncertainty and giving a usable number *now* is the whole role.

**"We have the trade, they don't."**
Then our records say it executed and theirs don't — so either it never reached them, or it
was rejected. Check the exchange's drop copy as an independent third source. **Name that
third source** — resolving a two-way disagreement needs a tiebreaker, and the exchange's own
record is it. Then: if it really didn't execute, our position is wrong and the desk thinks it
owns 200 shares it doesn't, which is a live risk to flag immediately, not a bookkeeping issue.

---

## Scenario 2 — P&L changed for a date that already closed

**The reframe that earns the point:** a report for a *past* date changing means either the
**inputs** changed or the **calculation** changed. There is no third option. That immediately
halves the search space, and saying it out loud is better than listing ten causes.

- **Inputs changed**: a late trade arrived; a trade was amended or busted; a mark was
  corrected; an FX rate was restated.
- **Calculation changed**: a deploy overnight; a config change; a different cost convention;
  a different snapshot time.

**Check first:** is the trade count for that date the same in both runs? One cheap query
splits inputs from calculation. If the count differs, it's inputs. If identical, suspect the
code or config, and `git log` since yesterday's run.

**The thing to flag unprompted:** a system that silently restates a closed day is itself the
bug. Historical reports should either be immutable or loudly versioned, because the desk made
decisions on the original number. *"Separately from this break — the fact that we can restate
a closed day without anyone being told is a problem worth fixing."* That's the kind of
observation that distinguishes a strong candidate.

$50k on $1.2M is ~4% — large enough to be a real trade, not a rounding artifact.

---

## Scenario 3 — stale price on the screen

**Bisect by evidence at each hop:** exchange → our feed handler → internal publisher →
the trader's application → the screen.

**Sequence numbers are the tool.** Say this explicitly:
- **Contiguous sequence numbers at the consumer** → nothing was lost in transit. The problem
  is downstream: the application's rendering thread, a UI freeze, a garbage collection pause,
  or deliberate conflation.
- **A gap** → data was lost upstream, and the gap's location tells you which hop.

**The follow-up — contiguous numbers but a 10-second cluster arriving at once — is the good
one.** That means nothing was *lost*, it was **delayed and then released in a burst**. That's
a buffering or backpressure problem, not a data loss problem. Candidate causes: a slow
consumer whose queue backed up, a GC pause, a network buffer filling, or a blocked write.
The signature to name: **the data is complete but the timestamps bunch**, which is exactly
what queueing looks like from the far end.

Also worth saying: the trader is almost certainly right that their screen was stale, *and*
your logs are almost certainly right that you published continuously. **Both can be true** —
that's what a downstream stall means. Starting from "who's wrong?" is the trap; the answer is
usually "nobody is lying."

---

## Scenario 4 — 42 duplicate trades

- **Find them**: group by trade ID and count > 1. If IDs are unique but the rows are
  identical on every other field, group by the natural key (symbol, side, qty, price,
  timestamp).
- **Cause**: at-least-once delivery plus a non-idempotent consumer. Classically a consumer
  crashed after processing but before acknowledging, so on restart it reprocessed. A
  producer retry after a timeout does the same thing.
- **Genuine vs duplicate**: you often *can't* tell from the data — two real trades can be
  identical in every field, which is common in liquid markets. The resolution is the
  **exchange-assigned unique trade ID**; if there isn't one, say that's the actual defect.
  (Same ambiguity as Mock 7's duplicate line — call out the connection.)
- **Fixes, both ends**: consumer-side, dedupe on trade ID with a seen-set (the real fix, and
  it makes the system robust regardless of the producer). Producer-side, don't retry blindly;
  make the write idempotent. **Say that consumer-side idempotency is the one you'd rely on**,
  because you control it and it defends against every producer.
- **Right now for the desk**: give risk the deduplicated count and tell them the number is
  10,000, before you've fixed anything.

---

## Scenario 5 — it might be your fault

What they're testing: honesty under pressure and whether you prioritize the desk over your
ego. The answer:

1. **Say so immediately.** "My change this morning is a candidate — I'm treating it as the
   leading hypothesis." Volunteering it is the whole test.
2. **Restore first, diagnose second.** Roll back to the known-good build, verify the break
   stops, *then* investigate. Do not debug forward in production while the desk is impaired.
3. **Communicate while it's ongoing**, not after: what's broken, what the impact is, what
   number they should use meanwhile, and when you'll next update them.
4. **Afterwards**: a blameless write-up, and the real question — how did a change that could
   cause this reach production without a test catching it?

The failure mode they're watching for is quietly investigating to find out whether it's your
fault before telling anyone. Say explicitly that you'd flag it before you know.

---

## The habits that score across all five
- **Quantify before hypothesizing.** "200 shares, one trade or many?" beats five theories.
- **Bisect** — in time, and along the pipeline.
- **Name the tiebreaker source** when two systems disagree.
- **Separate mitigation from root cause**, and give the desk a usable number immediately.
- **Say what evidence would disprove you.** A hypothesis without a test is a guess.
- **"Both can be true."** Most production mysteries are two correct systems measuring
  different things.
