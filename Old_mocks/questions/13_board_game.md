# Mock 13 — Board Game Implementation (~60 min)

Reported directly: *"Board game implementation coding exercise"* as an onsite round. This is
the same **escalating-implementation** shape as the order book, with rules instead of
matching. Everything you practised in Mock 5 transfers: ask first, pick structures
deliberately, keep the escalations cheap.

Why they like it: there's no domain knowledge to hide behind, the rules are unambiguous, and
they can keep adding requirements forever.

Set a 60-minute timer. Do not read ahead.

---

## Game A — Tic-tac-toe
> "Let's implement tic-tac-toe."

1. Represent the board. **Say why** you chose your representation — a 3x3 list of lists, a
   flat list of 9, a dict of coordinates, or two bitmasks. Any is defensible; the reasoning
   is the point.
2. `make_move(row, col, player)` — place a mark. What makes a move invalid?
3. `check_winner()` — return the winner, or `None`.
4. Detect a draw. **Is "board full with no winner" sufficient?** (Think about it before
   answering.)
5. Play a full game alternating turns.

Then the escalations, which arrive one at a time:
6. *"Now make it N x N, win by getting N in a row."*
7. *"Now it's N x N but you only need K in a row to win."* — this is the real question;
   your Part 3 approach probably doesn't survive it.
8. *"How would you check for a winner without rescanning the whole board after every move?"*
9. *"Write a bot that never loses."*
10. *"What's the complexity of each operation?"*

---

## Game B — Connect Four
> "Implement Connect Four — 7 columns, 6 rows, pieces fall to the lowest empty slot, four in
> a row wins in any direction."

The twist versus tic-tac-toe: **a move is a column, not a cell**, so you compute where the
piece lands. Escalations:
1. Drop a piece, reject a full column.
2. Detect four in a row — horizontal, vertical, both diagonals.
3. *"Only check around the piece just played."*
4. *"Undo the last move."*
5. *"Who wins with perfect play from this position?"* (describe, don't implement)

---

## Game C — Game of Life
> "Implement Conway's Game of Life: a cell with 2 or 3 live neighbours survives, a dead cell
> with exactly 3 live neighbours becomes alive, everything else dies."

Escalations:
1. One step on a fixed grid.
2. *"What about cells at the edges?"* — decide and defend: dead border, or wrapping?
3. **The classic trap**: *"Do it in place."* Why is the naive in-place version wrong?
4. *"The grid is a million by a million but only 100 cells are alive."* — this forces a
   complete change of representation, and it's the best question in the mock.

---

## What's actually being tested
Not game knowledge. They're watching whether you:
- ask about the rules before coding (what's a draw? can a move be taken back?),
- pick a representation **and justify it**, rather than typing the first thing,
- write the win check in a way that generalizes, rather than hard-coding eight lines of
  index comparisons,
- handle the "now make it bigger/faster/different" escalation without a rewrite.
