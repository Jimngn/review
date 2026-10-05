# Mock 12 — Trading System Inconsistency Debugging (~40 min)

Reported directly: *"Trading system inconsistency debugging"* as an onsite round. This is the
**most TDOE-specific question type that exists** — it's the actual job. Something doesn't
reconcile, the desk needs an answer, and you have to reason about where a distributed system
can disagree with itself.

There's usually no code to write. You're scored on **diagnostic structure**: do you narrow
systematically, or guess?

## The method to use every time, out loud
1. **Quantify it.** How big is the break? One trade or all of them? One symbol or many?
2. **Bound it in time.** When did it start? What else happened then?
3. **Establish the source of truth.** Which of the two disagreeing numbers do you trust, and
   why?
4. **Bisect the pipeline.** The data passes through N stages; check the middle one. Is the
   discrepancy already present there, or introduced after?
5. **Form one hypothesis, name the test that would disprove it.** Not three vague ones.
6. **Say what you'd do for the desk right now**, separately from the root cause. The trader
   needs a number before you need an explanation.

That last point is what separates a TDOE answer from an SWE answer. **Always split
"mitigate now" from "fix properly."**

---

## Scenario 1 — the position break
> "The desk's position system says we're long 5,000 AAPL. The clearing broker says 4,800.
> It's 9:45am and the trader wants to know which is right. Go."

Work through it out loud before reading the key. Some things to pin down:
- Is 200 shares one trade, or an accumulation of many?
- Does the break exist in yesterday's closing position, or did it appear today?
- What could legitimately differ between our view and theirs?

Follow-ups the interviewer will push:
- "The trader says he's about to do a big trade. What do you tell him?"
- "You find the missing trade in our log but not theirs. Now what?"
- "It turns out the number was fine yesterday. Does that change your approach?"

---

## Scenario 2 — the P&L that moved overnight
> "Yesterday's end-of-day P&L for a desk was $1.2M. This morning the same report for the
> same date says $1.15M. Nothing traded overnight. Why?"

Candidate causes to enumerate — the point is generating a *complete* list, then pruning:
- A trade was amended or busted after the close.
- The mark changed (a price correction, or a different source used in the rerun).
- A late trade arrived after the report ran.
- FX rates, if anything is non-USD.
- A code or config change deployed overnight.
- The two reports used different cost conventions or different cut-off times.

Then: "which of those would you check first, and what single query tells you?"

---

## Scenario 3 — the market data gap
> "A trader says their screen showed a stale price for ten seconds during the open, but our
> logs show we published updates continuously. Who's wrong?"

Reason about every hop between the exchange and the trader's screen, and about what evidence
would exist at each. Key concept: **sequence numbers**. If the consumer's sequence numbers
are contiguous, they received everything and the problem is downstream (rendering, their
machine, conflation). If there's a gap, it's upstream.

Follow-up: "the sequence numbers are contiguous but the timestamps show a 10-second cluster
arriving at once." What does that tell you?

---

## Scenario 4 — the duplicate trades
> "Our trade count for the day is 10,042. The exchange says 10,000. Risk is complaining."

- How would you find the 42 extra efficiently?
- What produces duplicates in a system that delivers at-least-once?
- If the duplicates have identical fields, how do you know they're duplicates rather than
  genuine repeated trades? (This is the same ambiguity as Mock 7's duplicate line — say so.)
- What's the fix at the consumer, and what's the fix at the producer?

---

## Scenario 5 — the one that's your fault
> "A change you deployed this morning is suspected of causing the break. How do you proceed?"

They are testing judgment and honesty, not technical skill. Have an answer about: saying so
immediately rather than quietly investigating; the fastest path to a known-good state
(roll back first, diagnose after); and communicating to the desk while it's ongoing.
