# Answer Key — Mock 4 (No-Execution Manual Tracing)

## Exercise 1 — remove_negatives
```python
def remove_negatives(nums):
    for i in range(len(nums)):
        if nums[i] < 0:
            del nums[i]
    return nums
```
Trace on `[1, -2, -3, 4]`. `range(len(nums))` is computed **once**, up front, as
`range(0, 4)` — it does not recheck `len(nums)` as the list shrinks.
- `i=0`: `nums = [1, -2, -3, 4]`, `nums[0] = 1`, not negative, nothing happens.
- `i=1`: `nums[1] = -2`, negative — `del nums[1]` → `nums = [1, -3, 4]`. The list just got
  shorter, and everything after index 1 shifted left by one.
- `i=2`: `nums[2]` is now `4` (because `-3` shifted into index 1, and `4` into index 2) —
  **`-3` was skipped entirely**, never checked, because the loop moved on to `i=2` while
  `-3` had shifted back to index 1. Not negative, nothing happens.
- `i=3`: but `nums` now only has 3 elements (indices 0-2) — `nums[3]` raises
  **`IndexError: list index out of range`**.

So the bug produces both a wrong answer (missed `-3`) *and* a crash, depending on how far it
gets — this is exactly the "mutating a list while iterating over it by index" trap from the
fundamentals edge-case checklist. **Fix**: don't delete from the list you're indexing into;
build a new one instead.
```python
def remove_negatives(nums):
    return [x for x in nums if x >= 0]
```

## Exercise 2 — average
```python
def average(nums):
    total = 0
    for i in range(1, len(nums)):
        total += nums[i]
    return total / len(nums)
```
Trace on `[10, 20, 30]`. `range(1, len(nums))` is `range(1, 3)`, i.e. `i = 1, 2` — **index 0
is never visited**.
- `i=1`: `total += nums[1]` → `total = 0 + 20 = 20`.
- `i=2`: `total += nums[2]` → `total = 20 + 30 = 50`.
- Return `50 / 3 ≈ 16.67`.

Correct average of `[10, 20, 30]` is `60 / 3 = 20`. The bug is the `range(1, ...)` — it
should be `range(0, len(nums))` (or just `range(len(nums))`, since `range`'s default start
is 0), so that `nums[0] = 10` is included. **Fix**:
```python
def average(nums):
    return sum(nums) / len(nums)
```

## Exercise 3 — most_common_word
```python
def most_common_word(words):
    counts = {}
    for word in words:
        counts[word] += 1
    return max(counts, key=counts.get)
```
Trace on `["a", "b", "a"]`.
- First iteration, `word = "a"`: `counts["a"] += 1` is shorthand for
  `counts["a"] = counts["a"] + 1` — but `counts` is `{}`, so `counts["a"]` (the read on the
  right-hand side) raises **`KeyError: 'a'`** immediately, before anything is ever stored.

This is the exact "counting into a dict without a default" trap — `+=` on a dict key
requires the key to already exist, unlike `.get()`, which lets you supply a default for the
not-yet-seen case. **Fix**:
```python
def most_common_word(words):
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return max(counts, key=counts.get)
```

## Exercise 4 — mystery (correct, read-only)
```python
def mystery(nums):
    result = []
    seen = set()
    for x in nums:
        if x not in seen:
            result.append(x)
            seen.add(x)
    return result
```
In one sentence: **it removes duplicates from a list while preserving the original order of
first appearance.**

Trace on `[3, 1, 4, 1, 5, 9, 2, 6, 5, 3]`:
| x | in seen? | action | result | seen |
|---|---|---|---|---|
| 3 | no | append, add | [3] | {3} |
| 1 | no | append, add | [3,1] | {3,1} |
| 4 | no | append, add | [3,1,4] | {3,1,4} |
| 1 | **yes** | skip | [3,1,4] | {3,1,4} |
| 5 | no | append, add | [3,1,4,5] | {3,1,4,5} |
| 9 | no | append, add | [3,1,4,5,9] | {3,1,4,5,9} |
| 2 | no | append, add | [3,1,4,5,9,2] | {...,2} |
| 6 | no | append, add | [3,1,4,5,9,2,6] | {...,6} |
| 5 | **yes** | skip | (unchanged) | (unchanged) |
| 3 | **yes** | skip | (unchanged) | (unchanged) |

Final output: `[3, 1, 4, 5, 9, 2, 6]`.

## Exercise 5 — pseudocode
A reasonable pseudocode answer (exact wording doesn't matter — the structure does):
```
1. Create an empty mapping from department name -> list of employee names.
2. For each employee record:
     a. Look up its department in the mapping (creating an empty list if it's the
        department's first employee seen so far).
     b. Add the employee's name to that department's list.
3. Create an empty list, "qualifying departments".
4. For each department in the mapping:
     a. If the number of employees in its list is greater than 1, add the department
        name to "qualifying departments".
5. Sort "qualifying departments" alphabetically.
6. Return "qualifying departments".
```
Data structure to reach for first, stated out loud: **a dictionary**, because the core
operation is "group employees by a key (department)" — the grouping pattern from
`../../01_fundamentals/07_practical_patterns.md`. The "sorted alphabetically" and
"more than one" requirements are just a filter and a `sorted()` call applied *after* the
grouping is done — worth explicitly separating "how do I organize the data" (step 1-2) from
"how do I answer the actual question given that organization" (step 3-6), since that
separation is usually the difference between a clean answer and a tangled one under time
pressure.
