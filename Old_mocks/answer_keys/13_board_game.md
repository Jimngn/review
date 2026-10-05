# Answer Key — Mock 13 (Board Game Implementation)

## Game A — tic-tac-toe

### Representation
```python
board = [[None] * 3 for _ in range(3)]
```
**Say the trap out loud as you type it**: `[[None] * 3] * 3` creates three references to the
*same* row, so writing one cell writes three. Catching that unprompted is a genuinely good
moment and costs you one sentence.

Alternatives worth naming in passing: a flat list of 9 (index `r*3+c`, simpler to copy); a
`dict` keyed by `(r, c)` (natural for sparse or very large boards — and it's the answer to
Game C's final escalation); bitmasks (fastest, overkill here).

### Win check — write the version that generalizes
The weak answer hard-codes eight comparisons. The strong answer builds the lines, because
**step 6 and 7 are coming**:
```python
def lines(board):
    n = len(board)
    for i in range(n):
        yield [board[i][j] for j in range(n)]      # rows
        yield [board[j][i] for j in range(n)]      # cols
    yield [board[i][i] for i in range(n)]          # main diagonal
    yield [board[i][n - 1 - i] for i in range(n)]  # anti-diagonal

def check_winner(board):
    for line in lines(board):
        if line[0] is not None and all(c == line[0] for c in line):
            return line[0]
    return None
```
That handles step 6 (N x N) with **no changes at all** — say so when the escalation lands.

### The draw question
"Board full and no winner" is sufficient *for tic-tac-toe*, but it's not the general answer:
a draw really means **no player can still win**, which can be true before the board fills.
Raising that distinction is exactly the kind of edge-case thinking being scored. For N x N
with K in a row, early-draw detection is genuinely hard — say that rather than pretending.

### Step 7 — K in a row on an N x N board (the real question)
The all-lines approach breaks: you now need every *window* of K consecutive cells in all four
directions. The clean formulation:
```python
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]       # E, S, SE, SW

def wins_at(board, r, c, k):
    """Did the piece at (r, c) complete k in a row?"""
    player = board[r][c]
    if player is None:
        return False
    n = len(board)
    for dr, dc in DIRECTIONS:
        count = 1
        for sign in (1, -1):                          # extend both ways
            rr, cc = r + dr * sign, c + dc * sign
            while 0 <= rr < n and 0 <= cc < n and board[rr][cc] == player:
                count += 1
                rr += dr * sign
                cc += dc * sign
        if count >= k:
            return True
    return False
```
**Four directions, not eight** — each direction and its opposite are the same line, which is
why the inner loop extends both ways. Candidates who write eight directions have a bug
waiting (they'll double-count the origin cell) and it's worth saying why you chose four.

### Step 8 — don't rescan the board
This is the same insight as step 7: **only the cell just played can have created a win**, so
check outward from it. That's O(K) per move instead of O(N²). Note the connection to the
order book: *"same idea as only touching the price levels an order actually crosses —
do work proportional to what changed, not to the size of the state."*

### Step 9 — a bot that never loses
Minimax: the current player maximizes, the opponent minimizes, recurse to terminal positions.
Tic-tac-toe's full tree is at most 9! = 362,880 nodes, so plain minimax is fine with no
pruning. Mention **alpha-beta pruning** as what you'd add for a bigger board, and
**memoization** on board state for repeated positions. You usually won't be asked to write it
— naming the algorithm and its cost is the ask.

### Complexity summary to recite
Move O(1); naive win check O(N²); incremental win check O(K); minimax O(b^d).

---

## Game B — Connect Four

**The landing calculation is the only new idea:**
```python
def drop(board, col, player):
    for row in range(len(board) - 1, -1, -1):     # bottom row upward
        if board[row][col] is None:
            board[row][col] = player
            return row
    raise ValueError("column is full")
```
Getting the direction right (scan from the bottom) is where people fumble live. Say it out
loud: *"gravity means I fill from the highest index up."*

Win check: `wins_at` from Game A with `k=4`, called at the landing square — **unchanged code**,
which is the payoff for writing it generally. Point that out.

**Undo** is the escalation worth preparing: keep a stack of `(row, col)` moves; undo pops and
clears. Note that undo is what makes a search bot practical — you mutate and un-mutate one
board instead of copying it at every node. That connects step 4 to step 5 and shows you see
where the question is going.

**Perfect play**: Connect Four is solved — the first player wins with optimal play starting
in the centre column. The approach is minimax with alpha-beta, a transposition table, and
move ordering from the centre outward. Describe it; don't implement it.

---

## Game C — Game of Life

### Edges
State the choice explicitly: **dead border** (cells outside are dead — simpler, finite) or
**toroidal wrapping** (`(r + dr) % rows`). Either is fine; not addressing it is not.

### The in-place trap — this is the question
Updating in place is **wrong** because Life is a simultaneous update: once you've modified a
cell, its neighbours compute their new state from a mix of old and new values. The standard
fix is a second grid.

If they insist on in-place with O(1) extra space, **the trick is to encode both states in one
value**: use 2 bits per cell, writing the new state into the second bit while still reading
the first.
```python
# bit 0 = current state, bit 1 = next state
for r, c in all_cells:
    live = sum(board[rr][cc] & 1 for rr, cc in neighbours(r, c))
    if (board[r][c] & 1 and live in (2, 3)) or (not board[r][c] & 1 and live == 3):
        board[r][c] |= 2                         # set the next-state bit
for r, c in all_cells:
    board[r][c] >>= 1                            # promote next to current
```
Knowing that two-pass bit trick is a legitimately strong answer. But **lead with "I'd use a
second grid because it's obviously correct"** and offer the trick as the constrained version —
reaching for the clever thing first reads as showing off.

### The million-by-million grid with 100 live cells
**The best question in this mock, and it's a representation question, not an algorithm one.**
A dense grid is 10¹² cells — impossible. Switch to a **set of live coordinates**:
```python
def step(live):
    counts = Counter(
        (r + dr, c + dc)
        for (r, c) in live
        for dr in (-1, 0, 1) for dc in (-1, 0, 1)
        if (dr, dc) != (0, 0)
    )
    return {cell for cell, n in counts.items()
            if n == 3 or (n == 2 and cell in live)}
```
The insight to state: **only cells adjacent to a live cell can possibly change**, so you
iterate over neighbours of live cells rather than over the grid. Cost drops from O(rows x
cols) to **O(live cells)** — from 10¹² to ~800. The grid can now be unbounded and even
negative coordinates work for free.

This is the same move as the order book's "work proportional to what changed" and the
incremental win check. **If you notice that pattern out loud across three different problems,
that is the strongest signal available in the whole mock.**

---

## Scoring yourself
- [ ] Asked about the rules before coding
- [ ] Justified the board representation rather than defaulting
- [ ] Wrote the win check so N x N needed no changes
- [ ] Used four directions extending both ways, not eight
- [ ] Spotted the `[[None]*3]*3` aliasing trap
- [ ] Reached "only check around the last move" without being walked there
- [ ] Switched representation for the sparse case instead of optimizing the dense one
