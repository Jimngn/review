# Trading System Inconsistency Debugging

Reported: "Trading system inconsistency debugging". This is the most TDOE-specific round
there is: two numbers that should agree don't, and you have to work out why, out loud.
They're testing **your method** more than whether you guess the exact cause.

**Time: 10 min per scenario.**

---

## The method (say these steps explicitly)

1. **Scope it.** Which symbol(s), account(s), time range? How big is the difference? Is it
   still happening or a one-off? **Is it hurting trading right now?** (If yes, contain first:
   tell the desk, maybe pause the strategy.)
2. **Identify the two sources** that disagree and which one you trust more and why. (The
   exchange/clearing is usually the source of truth for what traded.)
3. **Find the first point of divergence.** Line both up by time / trade ID. When did they
   last agree? What's the first record that differs?
4. **Use the size and shape of the difference as a clue.** A difference of exactly one
   trade's qty, or exactly 2x a trade, or a round factor like 100x points at specific causes.
5. **Form hypotheses, then check each one** with data. Say which you'd check first and why.
6. **Fix the immediate problem**, then the **root cause**, then **prevent it** (an alert, a
   check, or a reconciliation that would have caught it sooner).

## The usual suspects (run through these every time)
- **Missing** message (dropped, gap not detected, filtered out)
- **Duplicate** message (replay without dedupe, retry)
- **Wrong sign** (buy booked as sell)
- **Wrong quantity or price** (units: shares vs lots, cents vs dollars, decimal place)
- **Timing / cutoff** (timezone, end-of-day boundary, late message)
- **Correction or bust** not applied (or applied twice)
- **Reference data** (stock split, symbol change, wrong multiplier)
- **Stale data** (price feed stopped updating; system using an old snapshot)

---

## Scenario 1: Position break
> "Our position system says we're **long 500** AAPL. The clearing firm says **long 300**.
> Today's trades were all small 100-share orders. What do you do?"

## Scenario 2: P&L jump with no trades
> "At 2:15pm the desk's P&L on one stock jumped by **+$1.2M** in one second. Nobody traded
> that stock today. Traders are excited. Should they be?"

## Scenario 3: Everything doubled after a restart
> "After the positions service restarted at 11am, every trade from the morning shows up
> **twice** on the trader's blotter. Afternoon trades look fine."

## Scenario 4: Crossed book in our market data
> "Our internal view of the order book for MSFT shows best bid **$101.00**, best ask
> **$100.95**. The exchange says nothing unusual is happening."

## Scenario 5: Trades on the wrong day
> "A trade we did at 7:55pm New York time on Monday appears in **Tuesday's** P&L report, and
> Monday's report is short by that amount."

Work all five out loud using the method before scrolling.

<br><br><br><br><br><br><br><br><br><br><br><br>

---
---

## MODEL ANSWERS

### Scenario 1: Position break (+200)
- **Scope:** one symbol, difference is +200 (we think we're longer). When did they last
  agree? Probably start of day, so the break is in today's trades.
- **Trust:** clearing is independent and usually right about what actually traded.
- **Use the number:** 200 with 100-share trades means two extra buys of 100, **or** two
  missing sells of 100, **or one sell booked as a buy** (a −100 counted as +100 is a
  difference of 200). That last one is a great thing to point out.
- **Check:** reconcile today's trade list against clearing by trade ID:
  - IDs we have that clearing doesn't → **duplicates** or **trades that were busted**?
  - IDs clearing has that we don't → **missed messages** (a sequence gap?).
  - Same ID, different side → **sign bug**.
- **Fix:** correct the position (with the desk's knowledge), then fix the cause (dedupe,
  gap detection, mapping bug). **Prevent:** intraday automated reconciliation that alerts
  on any difference, not just end of day.

### Scenario 2: P&L jump with no trades
- No trades means the position didn't change, so **the price did**. P&L = position × price
  change, so check the **mark price** used.
- Check: did the price feed send a bad tick (e.g., $15.00 → $150.0, a decimal error)? Did
  it **stop updating** and then jump? Was there a **stock split / corporate action** the
  reference data didn't handle (a 2-for-1 split halves the price; if the position wasn't
  doubled, P&L shows a fake loss, or a fake gain if it's backwards)? Wrong FX rate for a
  foreign stock?
- Compare our price against an independent source for that time.
- **Should they be excited?** Not yet. A $1.2M move in one second with no news and no
  trades is much more likely a data problem than real money. Tell them that, kindly, and
  verify before anyone acts on it (a trader might *hedge* a fake P&L and create a real
  position).
- **Prevent:** alert on price moves above X% in one tick; cross-check marks against a second
  price source.

### Scenario 3: Everything doubled after a restart
- Strong clue: **only trades before the restart** are doubled. On restart, the service
  **replayed** the morning's messages to rebuild state, but the **blotter didn't dedupe**,
  or the service didn't reset state before replaying, so they were applied twice.
- Check: do the duplicates have the **same trade IDs**? If yes, it's a replay/idempotency
  issue. (Different IDs would mean the exchange really sent them twice. Much less likely.)
- Are **positions** doubled too, or just the display? Positions matter more. Check them first.
- **Fix:** dedupe by trade ID; make replay idempotent (start from a clean state, or skip IDs
  already applied). **Prevent:** a test that restarts the service mid-day and checks the
  totals match.

### Scenario 4: Crossed book in our market data
- The primer's rule: a crossing order **trades immediately**, so the real exchange book
  is never crossed. **Our copy is wrong.**
- Likely causes: we **missed a message** (a trade or a cancel that removed the $101 bid or the
  $100.95 ask), we processed messages **out of order**, or our view **combines two sources**
  (e.g., bids from one feed, asks from another, or two exchanges) that are out of sync.
- Check sequence numbers on the feed for a gap around when it crossed. Compare against
  a fresh **snapshot** from the exchange.
- **Fix:** resync from a snapshot. **Prevent:** alert whenever our book is crossed (it's a
  one-line check, `best_bid >= best_ask`, from coding problem 6) and on any sequence gap.
- Bonus: if a strategy trades off this book, it might think there's free money (buy at
  100.95, sell at 101). Make sure it can't act on a crossed book.

### Scenario 5: Trades on the wrong day
- **Timezone / cutoff bug.** 7:55pm New York (EDT) is **11:55pm UTC** Monday. In winter
  (EST) it would be 00:55 UTC **Tuesday**. Or the report's trading-day cutoff is set to
  something like 7pm, so late trades roll to the next day.
- Check: what timezone are timestamps stored in vs what the report uses? What's the defined
  cutoff for a "trading day"? Does it happen only for after-hours trades? Only since a
  daylight-saving change?
- **Fix:** store timestamps in UTC and define the trading-day boundary explicitly. **Prevent:**
  test with trades right at the boundary and across DST changes.

---

## The phrases that score
- "First, is this affecting live trading right now? If so, I'd tell the desk before I start
  digging."
- "Which of these two numbers do I trust more, and why?"
- "When did they last agree?"
- "The difference is exactly 200, which is 2 × 100. That smells like a sign flip or a
  duplicate."
- "I wouldn't fix the number by hand without understanding why. Otherwise it'll happen
  again tomorrow."
- "How would we have caught this automatically? I'd add an alert for X."
