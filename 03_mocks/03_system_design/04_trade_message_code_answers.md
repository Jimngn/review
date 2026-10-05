# Answers: Trade Message System Code

Each part adds a few lines to the previous one. The **full solution** at the bottom was run
against tests for every case below.

---

## Part 1: Positions
```python
def new_state():
    return {"positions": {}}            # (account, symbol) -> net qty

def signed_qty(trade):
    if trade["side"] == "BUY":
        return trade["qty"]
    return -trade["qty"]

def process_message(state, msg):
    key = (msg["account"], msg["symbol"])
    state["positions"][key] = state["positions"].get(key, 0) + signed_qty(msg)
```
Say out loud: "I'm using a tuple `(account, symbol)` as the key, buys add and sells subtract."

---

## Part 2: Duplicates
Remember every trade you've applied, keyed by `trade_id`:
```python
# in new_state():        "trades": {}      # trade_id -> the original message
# at the top of process_message:
    if msg["trade_id"] in state["trades"]:
        return                              # already applied, so ignore
    state["trades"][msg["trade_id"]] = msg
```
- Why a **dict** (not a set): Part 4 needs the original message to undo it. If you only
  needed "seen or not", a set would do. Saying that shows you're thinking ahead.
- This makes the service **idempotent**: processing the same message twice has the same
  effect as once.

---

## Part 3: Gaps
Track the next seq number you expect:
```python
# in new_state():   "expected_seq": 1,   "missing": []
# at the top of process_message:
    seq = msg["seq"]
    if seq < state["expected_seq"]:
        if seq in state["missing"]:
            state["missing"].remove(seq)    # late resend filling a gap: process it
        else:
            return                          # seen before, so it's a duplicate
    else:
        for s in range(state["expected_seq"], seq):
            state["missing"].append(s)      # everything we skipped over
        state["expected_seq"] = seq + 1
```
Trace seq 1, 2, 5, 3:
| msg seq | expected before | action | missing after | expected after |
|---|---|---|---|---|
| 1 | 1 | normal | [] | 2 |
| 2 | 2 | normal | [] | 3 |
| 5 | 3 | skipped 3, 4 | [3, 4] | 6 |
| 3 | 6 | 3 < 6 and in missing → remove, process | [4] | 6 |

Things to say:
- `range(expected, seq)` adds nothing when `seq == expected`, so the normal case needs no
  special code.
- The **late resend** case is the follow-up trap. A naive "if seq < expected: ignore"
  would throw away the exact message you asked the exchange to resend.
- Complexity: `x in list` is O(m) where m = number of missing. Usually tiny. Use a set if
  you're worried.

---

## Part 4: Busts
To undo a trade you need its account, symbol, side and qty, but the bust message only has
the ID. **That's why Part 2 stored the whole message.**
```python
# in new_state():   "busted": set(),   "errors": []
# after the seq check, before the NEW handling:
    if msg["type"] == "BUST":
        tid = msg["trade_id"]
        if tid not in state["trades"]:
            state["errors"].append((seq, "bust for unknown trade " + tid))
        elif tid in state["busted"]:
            pass                            # already undone; do nothing
        else:
            original = state["trades"][tid]
            key = (original["account"], original["symbol"])
            state["positions"][key] -= signed_qty(original)   # undo = subtract what we added
            state["busted"].add(tid)
        return
```
- **Order matters:** do the seq check first (all message types have seq), then branch on
  type. The trade_id duplicate check only applies to NEW messages. A BUST *reuses* T1's ID
  on purpose, so it would wrongly look like a duplicate if you checked it first.
- **Don't delete T1 from `trades`.** Keep the history; mark it busted. A later "bust T1"
  should be recognized as a repeat, not as an unknown trade.

---

## Full solution
```python
def new_state():
    return {
        "positions": {},      # (account, symbol) -> net qty
        "trades": {},         # trade_id -> original NEW message
        "busted": set(),      # trade_ids already busted
        "expected_seq": 1,    # next seq number we expect
        "missing": [],        # seq numbers skipped and not yet received
        "errors": [],         # (seq, reason)
    }

def signed_qty(trade):
    if trade["side"] == "BUY":
        return trade["qty"]
    return -trade["qty"]

def process_message(state, msg):
    # 1. sequence numbers: detect gaps and duplicates
    seq = msg["seq"]
    if seq < state["expected_seq"]:
        if seq in state["missing"]:
            state["missing"].remove(seq)
        else:
            return
    else:
        for s in range(state["expected_seq"], seq):
            state["missing"].append(s)
        state["expected_seq"] = seq + 1

    # 2. busts: undo the original trade
    if msg["type"] == "BUST":
        tid = msg["trade_id"]
        if tid not in state["trades"]:
            state["errors"].append((seq, "bust for unknown trade " + tid))
        elif tid in state["busted"]:
            pass
        else:
            original = state["trades"][tid]
            key = (original["account"], original["symbol"])
            state["positions"][key] -= signed_qty(original)
            state["busted"].add(tid)
        return

    # 3. new trades: skip duplicate trade IDs, then apply
    if msg["trade_id"] in state["trades"]:
        return
    state["trades"][msg["trade_id"]] = msg
    key = (msg["account"], msg["symbol"])
    state["positions"][key] = state["positions"].get(key, 0) + signed_qty(msg)
```

---

## Part 5: Verbal answers
1. **Restart:** replay the message log from the start of the day (or from a saved checkpoint
   of `state` plus the messages after it). Replaying is safe because the code is
   **idempotent**: seq numbers and trade IDs already seen are ignored. This is exactly the
   "everything doubled after a restart" bug in `03_debugging_inconsistencies.md`, prevented.
2. **CORRECT** = undo the old version, apply the new one. Subtract `signed_qty(old)`, add
   `signed_qty(new)`, and store the new version under the same trade ID. You reuse your bust
   logic, and you never edit history silently.
3. **O(1) per message** (dict/set lookups), except the `missing` list check (usually tiny).
   `trades` grows all day. That's fine for a day; at end of day, archive it and start fresh,
   since positions carry over but the trade-ID memory doesn't need to.
4. **Alerts:** `missing` not empty for more than a few seconds (a gap the resend didn't fix);
   any entry in `errors`; message rate dropping to zero during market hours (feed died);
   a position change that's unusually large; end-of-day positions not matching the clearing
   firm (reconciliation).
