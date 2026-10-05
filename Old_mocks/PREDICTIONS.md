# Predicted Questions — TDOE Final Round

**What this is based on**, so you can weigh it yourself:
1. **Jane Street's own materials sent to you** — `Resource/Order_20Book_20Basics_20Primer.pdf`
   and `Resource/TDOE_Interviewing_-_Intro_to_Python.pdf`. This is the strongest signal in
   the whole folder: firms don't send an order book primer unless they intend to ask about
   order books. Everything in that PDF is fair game and should be treated as assigned reading.
2. **Reported candidate experience** for this round (see `00_README.md` for the caveats —
   anonymous, secondhand, directionally useful, not a question bank).
3. **The structure of the role.** TDOE sits between the traders and the systems; the
   questions test operational judgment under escalation, not algorithmic cleverness.

4. **What the recruiter told you directly** (strongest and most recent signal):
   > "The upcoming interviews will be more technical in nature. Reading the Order Book Basics
   > document is the best way to prepare for one of the interviews, and the rest of the
   > interviews will be more coding based."

5. **Glassdoor reports you collected**, which are the first good evidence about the
   **onsite structure specifically** — see the next section. They change the picture
   substantially.

### Reading that carefully — it changes the emphasis

Two things follow, and they adjust what I wrote before the recruiter's note:

- **The order book is ONE interview, not the theme of the round.** "The rest will be more
  coding based" explicitly contrasts the others with it. Do not expect matching-engine
  concepts in the coding interviews; expect the data to be *trade-flavoured* (symbols, sizes,
  prices) because that's the house style, but the *concepts* tested will be dicts, lists,
  strings, sorting and top-k.
- **That one interview may be less code-heavy than a full matching engine.** You do not
  prepare for a 60-minute from-scratch build by *reading a document* — you prepare by coding.
  "Reading is the best way to prepare" points at **comprehension and scenario work**: here's a
  book, here's an incoming order, what trades happen, at what price, and what's the book
  afterwards. That is a very different session from "implement an exchange."

**So prepare both, weighted accordingly:** hand-simulation of the primer's rules until the
arithmetic is automatic (cheap, high confidence it's tested) *and* the build (more expensive,
still plausible — it's the natural coding version of the same interview). Mock 5's Part 4
trace and the `ORDER-BOOK-CONCEPT` mode of `INTERVIEWER_PROMPT.md` cover the first; Mocks 5
and 6 cover the second.

Confidence labels below are my judgment, not measured frequencies. Treat the **top tier as
near-certain in shape**, not in exact wording.

---

---

## The onsite format (from your Glassdoor reports)

Multiple independent accounts of the final round converge on **a half-day, three technical
rounds plus an informal lunch**:

> "in person final round (3 rounds, 2 trading system design 1 coding)"
> "I had 2 formal and 1 informal. The first was on design of trading systems and
> infrastructure — at a whiteboard. The second was a paired coding interview where you went
> through some order-book related content and data analysis (all pseudo code). The final was
> an informal lunch interview."
> "Board game implementation coding exercise, Stock Exchange system design white boarding,
> Trading system inconsistency debugging"
> "final onsite — goes into a long case study of designing order books"

**The headline: system design is probably the largest single component, not coding.** Two of
three technical rounds in one report; whiteboarding named in three others. My earlier
prediction treated this round as mostly implementation — that was wrong, and Mock 11 exists
to fix it.

### The likely shape of your day

| Slot | What | Prep |
|---|---|---|
| **Design 1** | Trading systems / infrastructure at a whiteboard. Order book case study, exchange design, or trade message system | **Mock 11** |
| **Design 2 or debugging** | Either a second design case, or "trading system inconsistency debugging" | **Mock 11, 12** |
| **Coding** | Paired, often **pseudocode on a whiteboard rather than a runnable editor**. Order-book content and data analysis, or a board game | **Mocks 5–8, 13** |
| **Lunch (informal)** | Generic questions, culture, your questions. Still evaluative | **Mock 9 Set E** |

Two details worth internalizing:
- **"All pseudo code."** Confirms the no-execution reports. Practise writing code you cannot
  run and defending it by hand-tracing. Mocks 4 and 10 are built for this.
- **Interviewers give terminology context before the final.** Reported as friendly and
  willing to explain trading terms. So you will not be failed for not knowing jargon —
  **but you will be expected to apply the order book primer, since they gave it to you.**

### The earlier rounds, for calibration
The reports describe a pipeline much like yours: take-home/OA (Excel, financial haircutting),
a brain-teaser/probability + behavioural phone screen ("why TDOE instead of SWE"), then a
coding screen (LeetCode-medium, sorting, Big-O). One report mentions a round requiring you to
**learn an unfamiliar language from its documentation on the spot** — your process is Python,
so this is deprioritized, but the transferable skill is real: **you may be handed
documentation for an unfamiliar library or API and asked to apply it immediately.** If that
happens, read the docs out loud, state what you think the function does, and check before
relying on it.

## Tier 1 — expect these (prepare until automatic)

| Prediction | Why | Mock |
|---|---|---|
| **Order book scenario work by hand**: given a book and an incoming order, produce the trades, the prices, and the resulting book | The recruiter says *reading* the primer is the best prep — that points at comprehension, not implementation | 5 (Part 4), interviewer `ORDER-BOOK-CONCEPT` |
| **Build a matching engine from scratch, escalating for ~60 min** | The coding version of the same interview. Still very plausible, just no longer the only reading | 5, 6 |
| **"At what price does the trade happen?"** — explicitly or by catching you getting it wrong | The primer states it twice. It is the designed trap. | 5 |
| **Price-time priority, including the time half** | Half of candidates handle price and fumble FIFO within a level. | 5 |
| **Partial fills + sweeping multiple levels + leftover rests** | The primer's third worked example, verbatim. | 5 |
| **Cancel an order, then "make it O(1)"** | The natural first escalation, and it has a real answer. | 5, 6 |
| **"What's the complexity?"** after every single thing you write | Reported repeatedly across rounds. | 9 |
| **Top-k over trade-like data** | Independently reported by two candidates in earlier rounds; recurs as "top 3 symbols/levels/movers." | 1, 8 |
| **Dict grouping and summing over trade records** | The bread-and-butter coding round. | 7, 8 |
| **A repeat of your round-2 questions, extended further** | The recruiter called the rest "more coding based"; this round is the same thing with longer escalation ladders | 1, 3, 7, 8 |
| **Whiteboard system design of a trading system** — exchange, order book case study, trade message system, or infrastructure | Named in 5 separate reports; possibly 2 of 3 onsite rounds | **11** |
| **Pseudocode on a whiteboard with no interpreter** | "all pseudo code" reported directly | 4, 10 |
| **"Why trading / why this role?" / "why TDOE instead of SWE?"** | Universal, and the TDOE-vs-SWE framing is reported verbatim | 9 |

## Tier 2 — likely (prepare properly)

| Prediction | Mock |
|---|---|
| **Modify an order's quantity or price**, with the queue-priority rule as the real question | 6 |
| **Market orders / IOC**, and what happens to the unfilled remainder | 6 |
| **Best bid/ask, spread, and total size at each price** | 6 |
| **String parsing of a trade or quote log, then "here's the messy version"** | 7 |
| **Edge cases fired at you cold**: zero quantity, empty book, duplicate IDs, self-trade | 6, 9 |
| **"Which data structure, and why?"** — dict vs heap vs sorted list, named trade-offs | 5, 9 |
| **"What if it doesn't fit in memory?"** → generators and streaming | 7, 10 |
| **Hand-tracing code with no interpreter** | 4, 10 |
| **Trading system inconsistency debugging** — a break between two systems, diagnose it | **12** |
| **Board game implementation**, escalated (tic-tac-toe -> N x N -> K in a row) | **13** |
| **Top 3 trades "without a helper function"**, and "what if there are long and short sells?" | 1 (Part 6) |
| **"Code an O(n) sorting algorithm for a short array"** — counting sort, and knowing why O(n) needs a non-comparison sort | 2 (Part 4) |
| **An informal lunch interview** that is still evaluative | 9 |

## Tier 3 — possible (know the shape, don't over-prepare)

- **Fill-or-kill** and the atomicity pre-check — the sharpest of the order-type escalations.
- **Self-trade prevention** and why wash trading matters.
- **Realized vs unrealized P&L**, FIFO vs average cost.
- **Float precision** as an explicit question rather than a trap you fall into.
- **Concurrency**: "two threads update the same position" — recognize the race, name
  single-writer, don't write locking code.
- **Multiple symbols** at once in the order book.
- **An opening auction / crossing price** ("what single price maximizes volume traded?") —
  low probability, genuinely harder, only worth a look once everything above is solid.
- A **debugging** question: here's code that's subtly wrong, find it. (Mock 4.)

## What I do *not* expect
- LeetCode-hard algorithms (DP, graphs, advanced trees). Reported consistently as "a
  lighter version of the SWE mock interviews."
- Writing a real heap or sort from scratch. You'll be asked *when* to use one, not to
  implement it.
- Heavy OOP design patterns, or web-scale systems design of the "design Twitter" variety.
  **Note the correction**: I previously listed systems design here as something *not* to
  expect. The Glassdoor reports show the opposite — whiteboard design of *trading* systems is
  a major component. What stays off the list is the generic FAANG-style distributed-systems
  interview; what's very much on it is designing an exchange, an order book system, or a
  trade message pipeline.
- Anything requiring library knowledge beyond the standard library — `collections` and
  `heapq` are the ceiling.

---

## The five sentences that earn the most points

Have these ready to deploy verbatim. Each one is short, and each signals something specific:

1. *"Just to confirm — does the trade execute at the resting order's price or the incoming
   order's?"* — in the first five minutes of the order book problem.
2. *"That's O(n) because of the scan; I'd make it O(1) by keeping a map from order ID to the
   order, with a linked list per price level so I can unlink without searching."*
3. *"I'll keep matching and resting as separate steps, since if you add an immediate-or-cancel
   order later it's the same matching logic without the resting step."*
4. *"I'd store prices as integer cents — floats don't compare exactly, and an exchange's whole
   job is comparing prices."*
5. *"There's an ambiguity here: [X] could mean two things. I'll assume [Y] and flag it — tell
   me if you'd rather I did it the other way."*
6. *(design rounds)* **"I'd persist the input message log rather than the state, and rebuild
   by replaying it — that gives us recovery, audit, and deterministic testing from one
   decision."** This single idea carries more weight than anything else in a design round.
7. *(debugging rounds)* **"Before I guess at the cause — how big is the break, and when did
   it start? And separately from root cause, here's the number I'd give the desk right now."**

## The five mistakes that cost the most
1. Trading at the **incoming** order's price.
2. Losing **time priority** inside a price level.
3. **Going silent** while you think. Narrate even false starts: *"my instinct is a heap, but
   let me check whether I need ordered iteration first."*
4. **Agreeing with the interviewer when they're wrong.** They test this deliberately —
   see Mock 10's A3 trap. Verify, then push back politely with your reasoning.
5. **Over-engineering Part 1.** Don't build a heap-backed, order-ID-mapped engine before
   they've asked for matching. Build the simple correct thing, *say* what you'd upgrade and
   when, and let them pull you there.
6. **Drawing boxes before scoping, in a design round.** Ten confident minutes designing a
   system nobody asked for. Spend the first five on requirements and explicit exclusions.
7. **A design with no failure modes.** For a TDOE role, "what breaks and how do you find out
   at 9:31am" is the job. A flawless happy path with no answer to that is an incomplete design.

---

## Running these against a live interviewer
`INTERVIEWER_PROMPT.md` turns a fresh Claude session into the interviewer: one escalation at
a time, no solutions given, complexity demanded after every answer, and a scored debrief at
the end. It has a mode for each shape above. Use it *after* you've attempted the written
mock cold — it's for rehearsing the performance, not for learning the material.

## Schedule (16 days; compress proportionally)

| When | Do |
|---|---|
| Days 1–2 | Re-read both PDFs in `../Resource/`. Then `../01_fundamentals/CHEATSHEET.md` and `../02_drills/`, timed. |
| Day 3 | **Mock 11 Case A** (exchange design) cold on a whiteboard. This is the biggest gap for most candidates — start it early. |
| Days 4–5 | **Mock 5** cold, 60 min, no execution. Review key. Redo any part you fumbled. |
| Day 6 | **Mock 6** on top of your own Mock 5 code, not the reference. |
| Day 7 | Rest, or re-read the primer only. |
| Day 8 | **Mock 11 Cases B and C** (trade message system, position/P&L). Then **Mock 12** (debugging). |
| Day 9 | **Mock 7** or **8**. Then **Mock 9 Sets A–C** out loud until reflexive. |
| Day 10 | **Mock 13** (board game) + **Mock 1 Part 6** (no-helper top 3, long/short). |
| Day 11 | **Mock 4** (hand-tracing) + **Mock 9 Sets D–E**. Write your three questions for them. |
| Day 12 | **Mock 11 Case A again**, cold — it's the single most likely onsite round. Then **Mock 2 Part 4** (O(n) sort). |
| Day 13 | **Mock 10 Dress Rehearsal**, both sessions, full conditions. |
| Day 14 | After-action review. Fix only the top 2 weaknesses it exposed. |
| Day 15 | Light: skim keys, re-read the primer, rehearse "why TDOE not SWE" aloud. |
| Day 16 | **Nothing technical.** Sleep. Confirm setup, camera, editor the night before. |

Compress proportionally if you have less time — but **do not skip Mock 11, Mock 5, or Mock
10.** Design is probably the largest part of your onsite; Mock 5 is the telegraphed question;
Mock 10 is the only one that tests you under real conditions.

**If you only have three days:** Mock 11 Case A, Mock 5, Mock 12. In that order.
