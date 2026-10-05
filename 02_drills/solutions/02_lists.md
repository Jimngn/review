# Solutions — Drill Set 2 (Lists)

## 1. Second largest
```python
def second_largest(nums):
    unique = sorted(set(nums), reverse=True)
    return unique[1]
```
`set(nums)` collapses duplicates, `sorted(..., reverse=True)` puts the largest first, so
index `1` is the second-distinct-largest. Simple and clear beats clever here. A one-pass
alternative (no sorting) if you want the O(n) version:
```python
def second_largest(nums):
    first = second = None
    for x in set(nums):
        if first is None or x > first:
            first, second = x, first
        elif second is None or x > second:
            second = x
    return second
```

## 2. Remove duplicates, preserve order
```python
def dedupe(items):
    seen = set()
    result = []
    for x in items:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result
```
This is the exact "dedupe while preserving order" pattern from
`../../01_fundamentals/07_practical_patterns.md`. `set(items)` alone would be wrong here —
it dedupes but doesn't preserve order.

## 3. Flatten a list of lists
```python
def flatten(list_of_lists):
    result = []
    for sublist in list_of_lists:
        for item in sublist:
            result.append(item)
    return result
```
Nested loop: outer over each sublist, inner over each item in that sublist. Comprehension
version: `[item for sublist in list_of_lists for item in sublist]` (reads left-to-right in
the same nesting order as the loop version — write the loop first if the comprehension order
is confusing).

## 4. Running total
```python
def running_total(nums):
    result = []
    total = 0
    for x in nums:
        total += x
        result.append(total)
    return result
```
Classic accumulator pattern: `total` persists across iterations, updated each step, and the
*current* value is recorded into `result` every iteration (not just at the end).

## 5. Rotate a list
```python
def rotate(lst, k):
    k = k % len(lst)          # handles k > len(lst), and k == 0
    return lst[-k:] + lst[:-k] if k != 0 else lst[:]
```
The last `k` elements move to the front. `lst[-k:]` grabs the last k elements, `lst[:-k]`
grabs everything before that. The `k % len(lst)` guards against `k` being larger than the
list length (rotating by the full length is a no-op) — and the `if k != 0` guard exists
because `lst[-0:]` is the same as `lst[0:]` (the *whole* list), not empty, so `k == 0`
needs to be handled separately to avoid `lst[-0:] + lst[:-0]` doubling the list.

## 6. Merge two sorted lists
```python
def merge_sorted(a, b):
    result = []
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])   # append whatever's left in a (no-op if a is exhausted)
    result.extend(b[j:])   # same for b
    return result
```
Two pointers (`i`, `j`), one into each list. At each step, take the smaller of the two
current elements and advance that pointer. When one list runs out, the loop stops and
whatever remains of the *other* list (already sorted) is appended wholesale — `a[i:]` is
just `[]` if `a` was the one that ran out, so no extra `if` is needed there.
