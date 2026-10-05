# Mocks — simulating the actual TDOE technical Zoom

## Why this folder exists
Candidate reports (Glassdoor, Reddit) about this specific round — the technical Zoom with
TDOEs, right after the take-home and the problem-solving/probability Zoom — converge on a
fairly narrow, consistent shape:

- **"Find the top three largest numbers in a list, then generalize to top k."** Reported
  independently by two different candidates (one explicitly framed around trade sizes).
  One report claimed the interviewer wanted "constant time" — that's almost certainly a
  mix-up; you must look at every element at least once (O(n)), so the real target is
  **O(n) time, O(1) extra space**, not sorting the whole list.
- **Live coding about sorting / merging**, with a team member watching and asking questions.
- **Basic pseudocode in a shared notepad**, with heavy emphasis on explaining your
  approach out loud and walking through edge cases — not necessarily raw syntax speed.
- **Possibly no code execution** — one report says code couldn't be run, meaning you may
  need to convince the interviewer your code is correct by tracing it by hand.
- Recruiter description (secondhand, one candidate): "a lighter version of the SWE mock
  interview videos" — i.e. don't expect LeetCode-hard, but do expect the same *format*
  (think out loud, handle follow-ups, defend your approach).

**Caveat, said plainly:** this is anonymous, secondhand candidate testimony, not a leaked
question bank. Treat everything here as a strong signal about *shape and style*, not a
guarantee of exact questions. The `../01_fundamentals/` and `../02_drills/` folders are the
foundation — this folder is where you rehearse the *format* on top of that foundation.

## How to run a mock session
1. Pick one file from `questions/`. Don't open the matching file in `answer_keys/` yet.
2. **Simulate the constraints that were reported**: use a plain text editor or a shared-doc
   style tool (not an IDE with autocomplete), and for at least one session, don't run your
   code at all — just write it and trace it by hand against the examples, the way you would
   in a no-execution CoderPad session.
3. Talk out loud the entire time, including:
   - Restating the problem and asking a clarifying question or two before coding (see each
     prompt's "questions worth asking" — try to come up with your own first).
   - Narrating your approach before writing code ("I'll do X because Y").
   - Walking through your code against the given example, and against at least one edge
     case, line by line, out loud — as if convincing someone else it's correct.
4. Each prompt has follow-ups baked in, the way a real interviewer would push after your
   first working answer (generalize it, make it faster, what if the input changes shape).
   Attempt the follow-up *before* reading the answer key's discussion of it.
5. Only then open `answer_keys/`. Compare not just correctness but whether you actually
   said the reasoning out loud, unprompted — that's the part self-study normally skips and
   the part this round seems to weight heavily.

## Files
Start with `PREDICTIONS.md` — it ranks what's most likely to come up, describes the **onsite
format** reconstructed from candidate reports, and gives a schedule for working through
everything below. **If you read one thing, read that.**

| Question | Mirrors | Time |
|---|---|---|
| `01_top_k_trades.md` | The most directly-reported question shape: largest -> top 3 -> top k | 30 min |
| `02_sorting_and_merging.md` | "Live coding about sorting algorithms" + merging report | 30 min |
| `03_trade_aggregation.md` | Dict counting/aggregation over trade-like records | 30 min |
| `04_no_execution_tracing.md` | The no-code-execution / manual-tracing / pseudocode report | 30 min |
| **`05_order_book_core.md`** | **The matching engine.** Jane Street sent you `../Resource/Order_20Book_20Basics_20Primer.pdf` — that is as close to a telegraphed question as this process gets | **60 min** |
| **`06_order_book_extensions.md`** | The escalation on top of your own Mock 5 code: cancel, modify, market/IOC/FOK, depth, self-trade | 45 min |
| `07_trade_log_parsing.md` | "Parsing strings" coding round, clean -> messy -> grouped -> at scale | 45 min |
| `08_positions_and_pnl.md` | "Grouping and summing with dictionaries" in real trading framing: positions, P&L, top movers | 45 min |
| `09_rapid_fire_verbal.md` | The complexity / data-structure / edge-case questions fired between tasks, plus your questions for them | 30 min |
| `10_dress_rehearsal.md` | Full simulated round, 2x60 min, fresh problem variants under real conditions | 2 hrs |
| **`11_system_design.md`** | **Whiteboard trading-system design** — exchange/order book, trade message system, position & P&L, market data. Named in 5 separate candidate reports; possibly 2 of 3 onsite rounds | 45–60 min each |
| **`12_system_debugging.md`** | "Trading system inconsistency debugging" — position breaks, P&L that moved, market data gaps, duplicate trades. The most TDOE-specific round that exists | 40 min |
| `13_board_game.md` | Board game implementation, escalated: tic-tac-toe -> N x N -> K in a row, Connect Four, Game of Life | 60 min |

## Live mock interviews
`INTERVIEWER_PROMPT.md` is a copy-pasteable prompt that makes a fresh Claude session act as
the interviewer — escalating one step at a time, never showing you what's coming, refusing to
write code for you, and ending with a scored debrief. Eight modes: `ORDER-BOOK-CONCEPT`,
`ORDER-BOOK-BUILD`, `SYSTEM-DESIGN`, `DEBUGGING`, `CODING`, `BOARD-GAME`, `RAPID-FIRE`, and
`ONSITE` (which simulates the full reported half-day: design, debugging, coding, lunch).

## Reference implementation
Two separate engines, so you can read the one you're working on without the other's
machinery in the way:

| File | Contains | Verified by |
|---|---|---|
| `reference/order_book_mock5.py` | **The core only** — book structures, print, matching, partial fills, cancel. Nothing from Mock 6. | `test_mock5.py` — all four primer worked examples |
| `reference/order_book_mock6.py` | Standalone full engine. Every addition marked `# +++ MOCK 6 +++` so you can see what each escalation cost | `test_mock6.py` |

Run `python3 test_mock5.py` (or `test_mock6.py`) from the `reference/` directory.

**Use it only after you've attempted the mock.** Reading the finished engine first is the
fastest way to feel prepared while learning nothing — the value is in hitting the escalations
cold and discovering where your own design breaks.

Do these **after** `../02_drills/`, not instead of it — the drills build the raw fluency,
these mocks build the interview *performance* on top of it.
