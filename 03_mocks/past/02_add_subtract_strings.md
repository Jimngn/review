# PAST QUESTION: Add Two Number Strings → Subtract

**This was asked in your previous technical round.** Redo it cold in a txt file, no running,
and trace by hand.

---

## The question

**Part 1.**
> "You're given two non-negative integers as strings, e.g. `"123"` and `"989"`. Return their
> sum as a string (`"1112"`). You may **not** convert the whole strings to integers."

**Part 2 (follow-up).**
> "Now do the same for **subtraction**: `a - b`."

Things to decide before coding:
- May I convert **one character** at a time? (Ask. Usually yes.)
- Can the result of subtraction be negative? (`"5" - "12"`?)
- Leading zeros in input? In output? (`"100" - "100"` should be `"0"`, not `"000"`.)
- Different lengths?

<br><br><br><br><br><br><br><br><br><br>

---
---

## ANSWERS

### The idea (say this before coding)
"Do it the way you'd do it on paper: start from the **rightmost** digit of each, add them
plus a carry, write down the last digit, carry the rest. Use two indices because the strings
can be different lengths. Build the result backwards, then reverse it."

### Single-digit conversion
```python
def digit(c):
    return ord(c) - ord("0")          # "7" -> 7, without int() on the whole string

def char(d):
    return chr(d + ord("0"))          # 7 -> "7"
```
If `ord` feels like a trick, `"0123456789".index(c)` and `"0123456789"[d]` do the same
thing. If they allow `int(c)` on single characters, that's fine too. **Ask.**

### Part 1: addition
```python
def add_strings(a, b):
    i = len(a) - 1
    j = len(b) - 1
    carry = 0
    result = []
    while i >= 0 or j >= 0 or carry > 0:
        total = carry
        if i >= 0:
            total += digit(a[i])
            i -= 1
        if j >= 0:
            total += digit(b[j])
            j -= 1
        result.append(char(total % 10))
        carry = total // 10
    result.reverse()
    return "".join(result)
```
Trace `"123" + "989"`:
| i | j | a[i] | b[j] | carry in | total | write | carry out |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 3 | 9 | 0 | 12 | 2 | 1 |
| 1 | 1 | 2 | 8 | 1 | 11 | 1 | 1 |
| 0 | 0 | 1 | 9 | 1 | 11 | 1 | 1 |
| -1 | -1 | – | – | 1 | 1 | 1 | 0 |
result reversed: `"1112"` ✓

Points to say:
- **`or carry > 0` in the loop condition** handles the final carry (`"99" + "1"` = `"100"`).
  Forgetting it is the #1 bug.
- `if i >= 0` handles different lengths without padding.
- Appending then reversing is O(n). Building with `char + result` each time is O(n²).
- Complexity: **O(max(len(a), len(b)))**.

### Part 2: subtraction
Plan: (1) strip leading zeros, (2) if a < b, compute b − a and add a `"-"`, (3) subtract digit
by digit with a **borrow**, (4) strip leading zeros from the result.

```python
def strip_zeros(s):
    i = 0
    while i < len(s) - 1 and s[i] == "0":     # keep at least one digit
        i += 1
    return s[i:]

def is_smaller(a, b):
    # a and b have no leading zeros
    if len(a) != len(b):
        return len(a) < len(b)                # fewer digits means smaller
    return a < b                              # same length: string compare works digit by digit

def subtract_strings(a, b):
    a = strip_zeros(a)
    b = strip_zeros(b)
    if a == b:
        return "0"
    if is_smaller(a, b):
        return "-" + subtract_strings(b, a)

    i = len(a) - 1
    j = len(b) - 1
    borrow = 0
    result = []
    while i >= 0:                             # a is the bigger one, so it's at least as long
        d = digit(a[i]) - borrow
        if j >= 0:
            d -= digit(b[j])
            j -= 1
        if d < 0:
            d += 10
            borrow = 1
        else:
            borrow = 0
        result.append(char(d))
        i -= 1
    result.reverse()
    return strip_zeros("".join(result))
```
Trace `"1000" - "1"`:
| i | a[i] | borrow in | b digit | d | write | borrow out |
|---|---|---|---|---|---|---|
| 3 | 0 | 0 | 1 | −1 → 9 | 9 | 1 |
| 2 | 0 | 1 | – | −1 → 9 | 9 | 1 |
| 1 | 0 | 1 | – | −1 → 9 | 9 | 1 |
| 0 | 1 | 1 | – | 0 | 0 | 0 |
reversed `"0999"` → strip → `"999"` ✓

Points to say:
- **Why compare first:** if a < b, borrowing runs off the left end. Swapping and adding a
  minus sign avoids that.
- **Why `a < b` works as strings only at equal length:** `"9" < "10"` is False as text, but
  with equal lengths, text order = number order.
- **Strip zeros at the end:** `"100" - "99"` produces `"001"`.

### Edge cases to test out loud
| Input | Expected |
|---|---|
| `add("0", "0")` | `"0"` |
| `add("99", "1")` | `"100"` (final carry) |
| `add("5", "12345")` | `"12350"` (different lengths) |
| `sub("100", "100")` | `"0"` |
| `sub("5", "12")` | `"-7"` |
| `sub("1000", "1")` | `"999"` (borrow chain) |
| `sub("007", "2")` | `"5"` (leading zeros in input) |

### Likely next follow-ups (verbal)
- **Negative inputs:** look at the signs. Same sign: add the magnitudes and keep the sign.
  Different signs: subtract the smaller magnitude from the bigger one and take the sign of the
  bigger. You reuse both functions.
- **Decimals (`"12.5" + "0.75"`):** split on `"."`, pad the fractional parts to the same
  length with zeros on the right, add the fractional parts first, and carry into the whole
  parts.
- **Why would anyone do this?** Numbers too big for a fixed-size integer, or money where
  you can't afford float rounding. Same reason prices are stored as integer cents.
- **Multiplication:** grade-school method, each digit of b times a, shifted and added.
  O(n·m). Describe it; don't code it unless asked.
