# Board Game Implementation: Tic-Tac-Toe → N × N → K in a Row

Reported as "board game implementation coding exercise". It tests the same skills as the
trade problems (2D lists, loops, careful indexing, edge cases) in a different costume.
Expect tic-tac-toe, built up one part at a time.

Plain text file, don't run it, trace by hand. **~45 min.** Answers:
`02_board_game_answers.md`.

Clarifying questions to ask at the start: How is a move given (row, col)? 0-indexed? Who
goes first? What should happen on an invalid move: reject it, or end the game?

---

## Part 1: The board
Write `new_board(n)` that returns an n × n board of empty cells (use `"."` for empty), and
`print_board(board)`:
```
X . O
. X .
. . .
```
Careful: there's a classic Python trap in building a 2D list. Know what it is.

---

## Part 2: Making a move
Write `make_move(board, row, col, player)`. It places `player` (`"X"` or `"O"`) and returns
`True`, or returns `False` **without changing the board** if the move is invalid.

What makes a move invalid? List every case before coding.

---

## Part 3: Who won? (3 × 3)
Write `winner(board)` that returns `"X"`, `"O"`, or `None`.

How many lines are there to check on a 3 × 3 board? Name them.

---

## Part 4: Play a whole game
Write `play(n, moves)`. `moves` is a list of `(row, col)`; X moves first and players
alternate. Return one of:
- `"X wins"` / `"O wins"`, as soon as someone wins
- `"draw"`: the board is full and nobody won
- `"in progress"`: moves ran out, board not full, no winner
- `"invalid move 4"`: the 4th move was invalid (1-based)

Trace it on:
```
play(3, [(0,0), (1,1), (0,1), (2,2), (0,2)])     # expect "X wins"
```

---

## Part 5: N × N
> "Now make `winner` work for any n × n board. You win with a full row, column, or diagonal."

What's the time complexity of checking the whole board?

---

## Part 6 (stretch): K in a row
> "Now the board is n × n but you only need **k** in a row to win (like 5-in-a-row on a
> 15 × 15 board)."

Write `has_k_in_a_row(board, player, k)`. Hint: from each cell, how many directions do you
need to check so you never miss a line and don't need to look backwards?

---

## Part 7: Verbal follow-ups
1. Checking the whole board after every move is wasteful. What's a faster check? (Think
   about what the **last move** can possibly have changed.)
2. How would you change this into **Connect Four** (pieces drop to the lowest empty row of a
   column)? Which function changes, and which ones stay the same?
3. How would you test this without running it? Which boards would you hand-check?
