# Mock 7 — Trade Log Parsing (escalating, ~45 min)

The "parsing strings" coding round. The pattern is always the same: a clean parse, then
messy data, then a question that's really about grouping, then a question that's really
about complexity. **Do not read ahead.**

Set a 45-minute timer. Plain editor. Narrate throughout.

---

## Part 1 — the clean parse (10 min)
> "Here's a log of today's trades, one per line."
```
AAPL,BUY,100,150.25
MSFT,SELL,50,380.10
AAPL,SELL,25,151.00
GOOG,BUY,10,2750.00
```
Write `parse(lines)` returning a list of records with symbol, side, quantity, price.

Before coding, ask: can I assume the format is always exactly this? Are quantities always
integers? Decide out loud what type each field becomes and why — **quantity to `int`, price
to `float` (or cents), symbol and side left as strings.** Mention that "150.25" stays a
string unless you convert it, and that a silent string-vs-number mix is the most common
source of bugs in this kind of problem.

---

## Part 2 — total notional (5 min)
> "What's the total dollar value traded?"

Notional = quantity x price, summed. Then:
> "Now per symbol."

---

## Part 3 — the data gets messy (15 min — the real test)
> "Turns out the log isn't clean. Here's the actual file."
```
AAPL,BUY,100,150.25
  MSFT , SELL , 50 , 380.10
AAPL,SELL,25,151.00

GOOG,BUY,ten,2750.00
TSLA,BUY,100
AAPL,buy,50,149.50
NVDA,BUY,-25,500.00
AAPL,SELL,25,151.00
```
Make `parse` robust. Each line here breaks something different — work out what each one is
testing before you touch the code:
- stray whitespace around fields
- a blank line
- a non-numeric quantity
- a line with a missing field
- lowercase side
- a negative quantity
- an exact duplicate of an earlier line

**The key question to ask out loud, and it's a real one:** *"Should a bad line be skipped,
reported, or should it stop everything?"* In a trading context the answer is rarely "crash,"
but it's also rarely "silently drop" — argue for collecting errors and returning them
alongside the good records, and say why: a silently dropped trade is a position you don't
know you have.

Decide explicitly whether that duplicate line is a **data error or a genuine second trade**
with identical details. There's no way to tell from the data alone — say that, and say what
you'd need (a trade ID or timestamp) to resolve it. Flagging the ambiguity is the answer.

---

## Part 4 — grouping (10 min)
> "Give me, per symbol: total bought, total sold, and the net position."

Then the escalation:
> "Now the volume-weighted average price per symbol."

VWAP = sum(qty x price) / sum(qty). Watch the division-by-zero case and say so before they
ask.

---

## Part 5 — the complexity and scale questions (5 min)
Be ready for all of these:
- What's the complexity of your parse? Of the grouping?
- "The file is 50 GB and doesn't fit in memory." What changes? (Name **streaming line by
  line with a generator**, and note which of your aggregations still work — sums and counts
  do; anything needing all records at once doesn't.)
- "Which symbol had the most volume?" — can you get it without sorting everything?
- "The lines are out of order and each has a timestamp." What changes?
