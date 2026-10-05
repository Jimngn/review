# Trade Message System: Write the Code

This is the coding half of `02_trade_message_system.md`. A design round can easily turn
into: *"OK, you're the positions service. Here's the stream of messages. Write the function
that handles them."* This exercise practices that.

Same rules as always: plain text file, don't run it, trace by hand, talk out loud. Reveal one
part at a time. **~35 min.** Answers: `04_trade_message_code_answers.md`.

---

## Setup
You're writing the **positions service**. It reads trade messages **one at a time** and keeps
each account's net position per symbol (buy = +, sell = −).

A message looks like:
```python
{"seq": 1, "type": "NEW", "trade_id": "T1", "account": "A",
 "symbol": "AAPL", "side": "BUY", "qty": 100, "price": 150.00}
```

You'll keep all your memory in one `state` dict and write
`process_message(state, msg)`, which updates `state` for **one** message. (One message at a
time, because in real life they arrive all day as a stream, not as a list.)

---

## Part 1: Positions
Write `new_state()` and `process_message(state, msg)` so that after processing these:
```python
msgs = [
    {"seq": 1, "type": "NEW", "trade_id": "T1", "account": "A", "symbol": "AAPL", "side": "BUY",  "qty": 100, "price": 150.00},
    {"seq": 2, "type": "NEW", "trade_id": "T2", "account": "A", "symbol": "AAPL", "side": "SELL", "qty":  30, "price": 151.00},
    {"seq": 3, "type": "NEW", "trade_id": "T3", "account": "B", "symbol": "MSFT", "side": "SELL", "qty":  50, "price": 300.00},
]
```
`state["positions"]` is `{("A", "AAPL"): 70, ("B", "MSFT"): -50}`.

---

## Part 2: Duplicates
> "Sometimes the same trade gets delivered twice (a network retry, or a replay after a
> restart). Right now that would double-count it. Fix it."

A duplicate has the same `trade_id`. Ignore it. Trace: T1, T2, T1 again → A's AAPL should
still be 70.

---

## Part 3: Gaps
> "Every message has a `seq` number that goes 1, 2, 3, ... with no holes. If we see seq 5 and
> then seq 8, we've **missed** 6 and 7. Track which seq numbers are missing."

Keep a list `state["missing"]`.
- Seq 1, 2, 5 → missing `[3, 4]`.
- If a seq number arrives that you've **already seen**, ignore it.

**Follow-up:** we ask the exchange to resend, and seq 3 arrives late, **after** 5. What should
happen? Make sure your code handles it: it should be processed and removed from `missing`.

---

## Part 4: Busts
> "An hour later the exchange **busts** (cancels) trade T1. It sends:"
```python
{"seq": 9, "type": "BUST", "trade_id": "T1"}
```
Undo T1's effect on the position. Think about:
- What do you need to have **stored** to undo a trade, when the bust message only has its ID?
- A bust for a trade ID you've **never seen**: don't crash. Record an error in
  `state["errors"]`.
- The same bust delivered **twice**: don't undo it twice.

---

## Part 5: Verbal follow-ups (no code needed)
1. The service crashes and restarts. How does it get its positions back? Why is replaying
   messages it already processed safe now?
2. The exchange sends a **CORRECT** message: "T2's qty was actually 40, not 30." How would you
   handle it using what you already wrote?
3. What's the time complexity per message? Does `state` grow forever? What would you do about
   that?
4. What would you **alert** on, so a human finds out something is wrong?
