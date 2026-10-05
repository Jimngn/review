# Debugging and Complexity — the bare minimum that matters

## Reading errors instead of fearing them
When code crashes, Python prints a **traceback** ending in the actual error. Read the *last
line* first — it names the error type and usually the exact problem.

| Error | Typical cause |
|---|---|
| `IndexError: list index out of range` | Indexed past the end (`lst[len(lst)]`), or looped one too far, or indexed an empty list/string |
| `KeyError: 'x'` | `d["x"]` where `"x"` isn't a key — use `.get()` if it might be missing |
| `TypeError: can only concatenate str (not "int") to str` | Mixed `str` and `int` with `+` — wrap with `str(...)` or use an f-string |
| `TypeError: 'NoneType' object is not iterable` (or similar) | A function returned `None` (often: forgot a `return`, or used `.sort()`/`.append()` expecting a return value) and you tried to use the result |
| `ValueError: invalid literal for int() with base 10` | Tried `int("abc")` or `int("")` — the string wasn't a valid number |
| `AttributeError: 'list' object has no attribute 'x'` | Called a method that doesn't exist on that type (e.g. `.keys()` on a list) — usually means you have the wrong data structure in mind |
| `NameError: name 'x' is not defined` | Typo'd a variable name, or used it before assigning it, or it's local to a different function |

Saying out loud "this is a KeyError, so some key I'm accessing doesn't exist, let me check
which one" is exactly the behavior an interviewer wants to see — it shows you can
self-diagnose without them hand-holding you.

## Debugging technique: print, don't guess
When something's wrong and it's not obvious why, add `print()` statements showing
intermediate values (loop variables, accumulator state) rather than staring at the code
trying to mentally simulate it. This is faster and more reliable under time pressure than
silent reasoning, and it's completely normal to do out loud in an interview.
```python
for i, x in enumerate(items):
    print(f"i={i} x={x} running_total={total}")   # temporary, delete before final answer
    total += x
```

## Testing your own function before declaring victory
Before saying "I'm done": call the function with (1) a normal example, (2) the smallest
possible input (empty list, empty string, single element), and trace the actual output
against what you expect. This catches the majority of bugs that would otherwise surface
only when the interviewer tries their own test case.

## Complexity — just enough intuition, no formal analysis needed
"Big-O" describes how the amount of work grows as input size `n` grows. You don't need to
derive it formally in this round — you need the *intuition* to avoid writing slow code and
to explain your choice if asked "can this be faster?"

- **O(1)** — constant time: dict/set lookup (`x in my_set`), indexing a list by position
  (`lst[i]`), appending to the end of a list.
- **O(n)** — one pass over the data: a single loop over a list of length n, `sum()`, `max()`,
  checking membership in a **list** (`x in my_list` — it has to scan).
- **O(n²)** — a loop inside a loop, each over the full data: comparing every pair of
  elements, or checking `x in my_list` *inside* a loop over that same list.

The one actionable takeaway: if you notice you've written a loop-inside-a-loop where the
inner loop is just "have I seen this value before" or "look this value up", that's almost
always a sign a dict/set turns it into a single pass. You don't need to name the complexity
out loud — just make the substitution when you spot the shape (see
`04_dictionaries_and_sets.md` for the worked example).

## When you're stuck
- Restate the problem in your own words out loud — this alone surfaces misunderstandings.
- Work a tiny example by hand first (on paper/in your head), *then* translate what you did
  by hand into code — don't try to jump straight to code for a problem you can't yet do
  manually.
- If a fully general solution isn't coming, write the brute-force version first (even an
  O(n²) one) — a correct, unoptimized answer is much better than no answer, and you can
  improve it afterward if time allows.
