# Control Flow

## Indentation is syntax
Python uses indentation (not braces) to mark blocks. Be consistent (4 spaces is standard).
Mixing tabs and spaces, or inconsistent indent levels, is a real syntax error — not a style
nitpick.

## if / elif / else
```python
if x > 10:
    print("big")
elif x > 0:
    print("small positive")
else:
    print("zero or negative")
```
No parentheses required around the condition (unlike C/Java), though `if (x > 10):` also
works — the parens are just ignored, not meaningful.

## Comparison and logical operators
```python
==   !=   <   >   <=   >=      # comparisons
and  or   not                   # logical operators (words, not && || !)

if x > 0 and x < 10:
    ...
if 0 < x < 10:      # Python allows chained comparisons — equivalent to the line above
    ...
if not found:
    ...
```

## while loops
```python
i = 0
while i < 5:
    print(i)
    i += 1          # no i++ in Python — use += 1
```
Use `while` when the number of iterations isn't known up front (e.g., "until a condition is
met"). Use `for` when iterating over a known collection or a fixed range — which is most of
the time in practical problems.

## for loops and range
```python
for i in range(5):          # 0, 1, 2, 3, 4  (stops BEFORE 5)
    print(i)

for i in range(2, 5):       # 2, 3, 4
    print(i)

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8  (step of 2)
    print(i)

for i in range(5, 0, -1):   # 5, 4, 3, 2, 1  (counting down needs a negative step)
    print(i)
```
**Gotcha:** `range(n)` never includes `n` itself. This is the same "stop is exclusive" rule
as slicing — internalize it once, it applies everywhere.

## break and continue
```python
for x in nums:
    if x < 0:
        continue      # skip the rest of this iteration, go to next x
    if x == 0:
        break          # exit the loop entirely
    print(x)
```

## Nested loops
```python
for i in range(3):
    for j in range(3):
        print(i, j)
```
Common in grid/matrix problems, or comparing every pair of elements. Watch for accidentally
writing O(n²) when a dict/set would make it O(n) — see `04_dictionaries_and_sets.md`.

## A pattern worth knowing: loop + accumulator
The vast majority of practical loop problems are: initialize a variable before the loop,
update it each iteration, use it after the loop.
```python
total = 0
for x in nums:
    total += x

best = None
for x in nums:
    if best is None or x > best:
        best = x
```
(Yes, `sum()` and `max()` already do this — but you should be able to write the manual
version instantly, because real problems are rarely *exactly* sum or max; they're a variant
of this shape with your own condition inside the loop.)
