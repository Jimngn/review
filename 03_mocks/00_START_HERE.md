# 03_mocks: Jane Street TDOE Final Round

This folder holds the **20% that covers 80% of the final round**. Everything else from
`Old_mocks/` is deliberately left out.

The job description says they don't expect you to know how to code beforehand. Your last
round confirms it: simple Python, a txt file, no running the code. The bar isn't clever
algorithms. It's whether you can **reason clearly and carefully out loud, catch your own
mistakes, and understand how trading systems behave.**

---

## What the day probably looks like

| Round | What it is | Folder |
|---|---|---|
| **A. Order book + data analysis** | Paired, pseudo code. They walk you through order-book content (the primer), then ask you to trace orders, build a tiny book, and analyze trade data. **The recruiter said the primer is the best prep for this one.** | `01_order_book/`, then `02_coding/` |
| **B. Design at a whiteboard** | "Design a stock exchange / order book", "design a trade message system", "trading system inconsistency debugging". Boxes, arrows, and good questions, **and expect to write some code** (the order book itself, or a message handler). Not FAANG distributed systems. | `03_system_design/`, `01_order_book/03_build_the_book.md` |
| **C. Coding** | Like your last round: a small problem in a text file, then follow-ups that each add one twist. Trade-shaped data, dicts, loops, strings. | `02_coding/`, `past/` |
| **Lunch** | Informal, but still part of the interview. Why TDOE, why Jane Street, your questions for them. | `04_lunch/` |

The order may differ and rounds may blend. The order book shows up everywhere, so it's
first.

---

## The 20%: know these cold

**Order book (01)**
- [ ] Bid = buy, offer/ask = sell. Best bid = highest bid. Best ask = lowest ask.
- [ ] A trade happens when bid price >= ask price ("equal or cross").
- [ ] **The trade executes at the RESTING order's price**, not the incoming order's.
- [ ] Price-time priority: better price first; at the same price, earlier first.
- [ ] One order can produce: no trade, one trade, several trades, or a partial fill. Any
      leftover **rests on the book** at its own limit price.
- [ ] After matching, the book is never crossed (best bid < best ask).
- [ ] You can hand-trace any scenario and write the matching loop in pseudo code.

**Coding (02)**
- [ ] Loop and track the best so far (max, top 3).
- [ ] Dict for counting, summing, and grouping (volume per symbol, position per trader).
- [ ] Parse a line with `split(",")` and convert types.
- [ ] Validate data: check each rule and collect the errors, don't crash.
- [ ] Compare two lists of records (reconciliation).
- [ ] Say the time complexity of what you wrote in one sentence.

**Design (03)**
- [ ] Draw an exchange: gateway → risk checks → sequencer → matching engine → fills +
      market data + audit log.
- [ ] Trade message: unique trade ID, sequence numbers, duplicates and gaps, corrections.
- [ ] Write the positions-service handler: dedupe by trade ID, detect seq gaps, apply busts.
- [ ] Debugging method: scope it, compare two sources, find the first difference,
      explain it, fix it, prevent it.

**Lunch (04)**
- [ ] A 60-second "about me", "why TDOE and not SWE", and 3 real questions for them.

---

## What's deliberately NOT here (skip it)

- LeetCode-style algorithms, recursion tricks, dynamic programming, graphs
- Writing a heap from scratch (just know "min-heap of size k" as an idea)
- Classes and OOP-heavy designs (a dict and two lists is a fine order book)
- Market/IOC/FOK/iceberg order types, self-trade prevention, auctions. If asked, give a
  sentence and move on.
- Distributed-systems theory (consensus, CAP, Kafka internals)
- OCaml

---

## How to practice (this matters more than the content)

Do every problem the way the real round runs:

1. **Plain text editor, no running the code.** Trace it by hand.
2. **Talk out loud the whole time**, even alone.
3. Follow this loop for every problem:
   1. **Restate** the problem and ask 1–2 clarifying questions.
   2. **Work a small example by hand** before writing code.
   3. **Say the approach in English** ("I'll keep a dict from symbol to total volume...").
   4. **Write it.** Pseudo code is fine; clean Python is better.
   5. **Trace your code** on the example, line by line, out loud.
   6. **Edge cases:** empty input, ties, one element, negatives, bad data.
   7. **Complexity** in one sentence.
4. Only then open the answers file.

For a live mock, paste `INTERVIEWER_PROMPT.md` into a fresh Claude session.

---

## Suggested order

| Session | Do | Time |
|---|---|---|
| 1 | `01_order_book/01_rules.md`, then `02_scenarios.md` (all 10) | 60 min |
| 2 | `01_order_book/03_build_the_book.md` | 60 min |
| 3 | `02_coding/00_patterns.md`, then problems 1–5 | 60 min |
| 4 | `02_coding/` problems 6–10, then `02_board_game.md` | 75 min |
| 5 | `past/` (redo both cold), then `03_system_design/` 00–02 | 75 min |
| 6 | `03_system_design/03_debugging_inconsistencies.md` + `04_trade_message_code.md` | 60 min |
| 7 | `04_lunch/`, then a full mock with `INTERVIEWER_PROMPT.md` in mode `FULL` | 90 min |
| Night before | Re-read `01_order_book/01_rules.md` and the checklist above. Nothing new. | 15 min |

---

## Folder map

```
03_mocks/
├── 00_START_HERE.md            ← you are here
├── INTERVIEWER_PROMPT.md       ← paste into a fresh Claude session for a live mock
├── 01_order_book/              ← Round A (primer round): highest priority
│   ├── 01_rules.md             ← the primer on one page + the traps
│   ├── 02_scenarios.md         ← 10 hand-trace drills + concept checks
│   ├── 02_scenarios_answers.md
│   ├── 03_build_the_book.md    ← pseudo-code the matching engine step by step
│   └── 03_build_the_book_answers.md
├── 02_coding/                  ← Rounds A and C: data analysis on trades
│   ├── 00_patterns.md          ← the 7 patterns + no-run gotchas
│   ├── 01_problems.md          ← 10 problems with follow-ups
│   ├── 01_answers.md
│   ├── 02_board_game.md        ← tic-tac-toe → N×N → k in a row
│   └── 02_board_game_answers.md
├── 03_system_design/           ← Round B: whiteboard
│   ├── 00_how_to_whiteboard.md
│   ├── 01_design_an_exchange.md
│   ├── 02_trade_message_system.md
│   ├── 03_debugging_inconsistencies.md
│   ├── 04_trade_message_code.md  ← the design turned into code: dedupe, gaps, busts
│   └── 04_trade_message_code_answers.md
├── 04_lunch/
│   └── lunch_and_behavioral.md
└── past/                       ← your actual previous-round questions
    ├── 01_top_k_trades.md
    └── 02_add_subtract_strings.md
```
