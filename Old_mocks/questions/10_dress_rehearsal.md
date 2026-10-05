# Mock 10 — Dress Rehearsal (full simulated round, 2x 60 min)

Run this **once, 3–4 days before the real thing**, start to finish, no pauses. The problems
are deliberately *variants* of Mocks 5–8 rather than repeats, so you're practising the skill
instead of recalling the solution. Don't read this file before the day you run it.

**Setup to match the real conditions:**
- Webcam on, dressed as you would be. Say your answers out loud to the camera.
- Plain shared-doc-style editor. **No autocomplete, no linter, no running the code** for
  Session A.
- A single 2-minute break between sessions. No notes, no reference files open.

---

# SESSION A — the build (60 min, no code execution)

## A1 (5 min) — warm-up, verbal
> "Walk me through what happens, step by step, when you send a limit order to an exchange
> and there's nothing on the other side of the book."

## A2 (40 min) — build it
> "Let's build a simple exchange. Orders have a side, a price, and a size. I want to be able
> to send orders in and see trades come out."

Same core as Mock 5, but the escalations arrive in a **different order** — handle them as
they come:
1. Match and print trades. Partial fills. Leftover rests.
2. *"Add a way to see the total size resting at the best bid and best offer."*
3. *"Now let orders be cancelled."*
4. *"A trader wants to **replace** an order — same ID, new price and new size. What
   happens to their queue position?"*
5. *"Add an order type that must fill completely right now or not at all."*
6. *"What if the same trader ends up on both sides?"*

## A3 (15 min) — defend it, with no interpreter
> "I can't run this. Convince me it's correct."

Hand-trace this sequence out loud, writing the book state after each step:
```
add  A  BUY   10.00  x100
add  B  BUY   10.00  x50
add  C  BUY    9.99  x200
add  D  SELL  10.01  x75
cancel A
add  E  SELL  10.00  x120
```
State after each line: the full book, and every trade with its price, quantity, and which
two order IDs matched. **Then** check it against `../reference/order_book_mock5.py`.

Expected if you're right: cancelling A promotes B to the front at 10.00; E trades 50 against
B at $10.00, then 70 against C at $9.99 — wait, does it? Work out whether E crosses C at all
before you accept that. **That trap is the point of the exercise.**

---

# SESSION B — the coding round (60 min, code execution allowed)

## B1 (25 min) — the data problem
> "Here's a feed of quote updates, one per line: symbol, bid, ask, timestamp."
```
AAPL,150.00,150.05,09:30:01
MSFT,380.00,380.10,09:30:01
AAPL,150.02,150.04,09:30:02
AAPL,150.10,150.12,09:30:05
MSFT,379.95,380.20,09:30:07
```
Escalating asks, one at a time:
1. Parse it.
2. "What's the latest quote for each symbol?"
3. "What's the average spread per symbol?"
4. "Which symbol had the **widest** spread at any point, and when?"
5. "Which symbols had their spread **widen** from one update to the next?" (This one needs
   previous-value state per symbol — think before you type.)
6. "The feed has 400 million lines. What changes?"

## B2 (25 min) — the ranking problem
> "Given a day of trades — symbol, size, price — give me the 3 symbols with the highest
> total traded value."

Then:
1. "What if there are ties?"
2. "What if I want the top 3 by number of trades instead?"
3. "What if I want the top 3 for every hour of the day?"
4. "What's the complexity, and what if there are 500,000 distinct symbols?"

## B3 (10 min) — their questions, then yours
Answer out loud: *"Why trading? Why this role?"* Then ask your three prepared questions.

---

## After-action review
Write down, honestly, before checking any key:
1. Where did you go silent for more than 20 seconds?
2. Which escalation forced you to change code you'd already written? Could a question in
   the first five minutes have prevented it?
3. Which complexity did you state only after being asked, rather than volunteering?
4. What did you get wrong in the A3 hand-trace, and why?

Those four answers are worth more than redoing any of the problems.
