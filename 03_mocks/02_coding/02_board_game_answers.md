# Answers: Board Game

All code here was run against tests (wins in every row, column and diagonal, draws, invalid
moves, k in a row, Connect Four drops).

---

## Part 1: The board
```python
def new_board(n):
    board = []
    for _ in range(n):
        board.append(["."] * n)        # a NEW list for every row
    return board

def print_board(board):
    for row in board:
        print(" ".join(row))
```
**The trap:** `[["."] * n] * n` makes **n references to the same row**. Setting
`board[0][0] = "X"` would put an X in the first column of *every* row. Say this out loud
when you write `new_board`; it's exactly the kind of bug they want you to know about when
code can't be run.

---

## Part 2: Making a move
Invalid if: row or col **out of bounds** (including negative!), cell **already taken**,
or player isn't `"X"`/`"O"`.
```python
def make_move(board, row, col, player):
    n = len(board)
    if player != "X" and player != "O":
        return False
    if row < 0 or row >= n or col < 0 or col >= n:
        return False
    if board[row][col] != ".":
        return False
    board[row][col] = player
    return True
```
Why check negative indexes: `board[-1]` is **valid Python** (the last row), so a move at
`(-1, 0)` would silently land on the bottom row instead of being rejected.

---

## Part 3: Who won? (3 × 3)
8 lines: 3 rows, 3 columns, 2 diagonals.
```python
def winner(board):
    lines = []
    for i in range(3):
        lines.append([board[i][0], board[i][1], board[i][2]])   # row i
        lines.append([board[0][i], board[1][i], board[2][i]])   # column i
    lines.append([board[0][0], board[1][1], board[2][2]])       # diagonal
    lines.append([board[0][2], board[1][1], board[2][0]])       # anti-diagonal
    for line in lines:
        if line[0] != "." and line[0] == line[1] and line[1] == line[2]:
            return line[0]
    return None
```
Don't forget `line[0] != "."`: otherwise an empty row "wins" for `"."`.

---

## Part 4: Play a whole game
```python
def board_full(board):
    for row in board:
        for cell in row:
            if cell == ".":
                return False
    return True

def play(n, moves):
    board = new_board(n)
    player = "X"
    for i in range(len(moves)):
        row, col = moves[i]
        if not make_move(board, row, col, player):
            return "invalid move " + str(i + 1)
        w = winner_n(board)              # Part 5 version, so any n works
        if w is not None:
            return w + " wins"
        if player == "X":
            player = "O"
        else:
            player = "X"
    if board_full(board):
        return "draw"
    return "in progress"
```
Trace `play(3, [(0,0), (1,1), (0,1), (2,2), (0,2)])`:
| move | player | board row 0 | winner? |
|---|---|---|---|
| (0,0) | X | X . . | no |
| (1,1) | O | X . . | no |
| (0,1) | X | X X . | no |
| (2,2) | O | X X . | no |
| (0,2) | X | X X X | **X** → `"X wins"` |

Points to say:
- Check for a winner **before** checking for a draw. The last move can fill the board *and*
  win, and that's a win, not a draw.
- Moves listed after the win are ignored. Mention it, or ask whether they should be an
  error.

---

## Part 5: N × N
```python
def winner_n(board):
    n = len(board)
    lines = []
    for i in range(n):
        row = []
        col = []
        for j in range(n):
            row.append(board[i][j])
            col.append(board[j][i])
        lines.append(row)
        lines.append(col)
    diag = []
    anti = []
    for i in range(n):
        diag.append(board[i][i])
        anti.append(board[i][n - 1 - i])
    lines.append(diag)
    lines.append(anti)

    for line in lines:
        if line[0] != "." and line.count(line[0]) == n:
            return line[0]
    return None
```
- `line.count(line[0]) == n` means every cell matches the first one.
- Anti-diagonal is `board[i][n - 1 - i]`. Check it on 3 × 3: (0,2), (1,1), (2,0). ✓
- Complexity: 2n + 2 lines × n cells = **O(n²)**, i.e. every cell a constant number of times.

---

## Part 6 (stretch): K in a row
From each cell, only look in **4 directions**: right, down, down-right, down-left. The
other 4 (left, up, ...) are the same lines seen from the other end, so they'd be checked
from the line's other end anyway.
```python
def has_k_in_a_row(board, player, k):
    rows = len(board)
    cols = len(board[0])
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]   # right, down, down-right, down-left
    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                count = 0
                rr = r
                cc = c
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == player and count < k:
                    count += 1
                    rr += dr
                    cc += dc
                if count == k:
                    return True
    return False
```
- Using `rows`/`cols` separately (not just n) means it also works for Connect Four's 6 × 7.
- The bounds check comes **first** in the `while` so `board[rr][cc]` is never read out of
  range (and never wraps around through negative indexes).
- Complexity: O(rows × cols × k).

---

## Part 7: Verbal answers
1. **Only check through the last move.** A new win must include the piece just placed. From
   the last move, for each of the 4 directions, count matching pieces going forward and
   backward. If 1 + forward + backward ≥ k, it's a win. That's O(k) per move instead of
   scanning the whole board.
   ```python
   def wins_through(board, row, col, k):
       player = board[row][col]
       rows = len(board)
       cols = len(board[0])
       for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
           count = 1                                   # the piece just placed
           for sign in [1, -1]:                        # forward, then backward
               r = row + sign * dr
               c = col + sign * dc
               while 0 <= r < rows and 0 <= c < cols and board[r][c] == player:
                   count += 1
                   r += sign * dr
                   c += sign * dc
           if count >= k:
               return True
       return False
   ```
2. **Connect Four:** only *placing* a piece changes. A move is just a column; the piece drops
   to the lowest empty row. Win checking is `has_k_in_a_row(board, player, 4)` on a 6 × 7
   board, unchanged. Good design point to make: "separate *how pieces get placed* from *how
   wins are checked*, and only one has to change."
   ```python
   def drop(board, col, player):
       for row in range(len(board) - 1, -1, -1):   # bottom row up
           if board[row][col] == ".":
               board[row][col] = player
               return row
       return None                                  # column is full: invalid move
   ```
3. **Hand tests:** a win on each row, each column, each diagonal; a full board with no
   winner (draw); a move on a taken cell; a move off the board, including a negative
   index; a win on the very last move (win, not draw).
