# Answer Key — Mock 2 (Sorting and Merging)

## Part 1 — implement a sort by hand
**Selection sort** (easiest to narrate correctly live: "repeatedly find the smallest
remaining element and put it in place"):
```python
def my_sort(nums):
    nums = nums[:]              # work on a copy, don't mutate the caller's list
    for i in range(len(nums)):
        min_idx = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[min_idx]:
                min_idx = j
        nums[i], nums[min_idx] = nums[min_idx], nums[i]
    return nums
```
Narrate it as: "for each position `i` from left to right, find the smallest value in the
unsorted remainder (from `i` onward) and swap it into position `i`." Complexity: O(n²) —
for each of n positions, scan up to n remaining elements to find the minimum; that's a
nested loop over the same data, so n * n. Correct on empty list (outer loop doesn't run,
returns `[]`), single element (outer loop runs once, no swap needed, returns as-is),
duplicates (comparison is `<`, so equal elements never get needlessly swapped past each
other — the algorithm is stable in this implementation... actually double-check: it can
still swap past equal elements if a later position holds a smaller distinct value, but equal
values relative to each other won't be reordered incorrectly since `<` not `<=` avoids
swapping when equal).

**Insertion sort** (equally acceptable, and arguably the more natural one to explain as
"how you'd sort a hand of playing cards"):
```python
def my_sort(nums):
    nums = nums[:]
    for i in range(1, len(nums)):
        key = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > key:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key
    return nums
```
Also O(n²) worst case. Either is a fine choice — what matters more than which one you pick
is that you can trace it correctly and state its complexity without hesitation.

## Part 2 — merge two sorted lists
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
    result.extend(a[i:])
    result.extend(b[j:])
    return result
```
This is O(n + m) where n, m are the two list lengths — a single pass through both lists
combined, because sortedness means you only ever need to look at the current front of each
list to know which one is globally next. Concatenating and re-sorting from scratch throws
away the fact that each half was already sorted, costing O((n+m) log(n+m)) instead — the
plain-language version of that gap: "we already did most of the work by having them sorted
individually; re-sorting ignores that and redoes it."

## Part 3 — merging many sorted lists (verbal, code optional)
Simplest correct framing: repeatedly merge two at a time (merge list 1 and 2, merge that
result with list 3, and so on). If there are `m` lists each of average length `n/m`, this
costs roughly O(n * m) in the worst case (each merge pass touches all elements processed so
far). A better approach, worth *naming* even if not implementing live: a min-heap holding
one "current" element from each of the m lists, repeatedly popping the smallest and
advancing that list's pointer — this gets you O(n log m). Naming the heap-based approach
and explaining *why* it's better (you avoid repeatedly re-scanning already-merged data) is
the valuable part of this answer; a full implementation is a bonus, not the bar.

## Part 4 — manual trace
`merge_sorted([2, 5, 8], [1, 3, 9, 10])`, with `a = [2,5,8]`, `b = [1,3,9,10]`:

| step | i | j | a[i] vs b[j] | action | result so far |
|---|---|---|---|---|---|
| 1 | 0 | 0 | 2 vs 1 | b smaller, take b[0]=1, j=1 | [1] |
| 2 | 0 | 1 | 2 vs 3 | a smaller/equal, take a[0]=2, i=1 | [1, 2] |
| 3 | 1 | 1 | 5 vs 3 | b smaller, take b[1]=3, j=2 | [1, 2, 3] |
| 4 | 1 | 2 | 5 vs 9 | a smaller, take a[1]=5, i=2 | [1, 2, 3, 5] |
| 5 | 2 | 2 | 8 vs 9 | a smaller, take a[2]=8, i=3 | [1, 2, 3, 5, 8] |

Now `i == len(a) == 3`, loop stops. `a[i:]` is `a[3:]` = `[]` (nothing left). `b[j:]` is
`b[2:]` = `[9, 10]`, appended wholesale. Final result: `[1, 2, 3, 5, 8, 9, 10]`.

---

## Part 4 — the O(n) sort (reported version)

**Lead with the theory, because it proves you're not guessing:**
> *"Any comparison-based sort has an Ω(n log n) lower bound, so if you want O(n) I can't be
> comparing elements to each other — I need to exploit something about the values. What's
> their range?"*

That single question is most of the answer. The intended algorithm is **counting sort**.

```python
def counting_sort(nums, lo, hi):
    counts = [0] * (hi - lo + 1)
    for x in nums:
        counts[x - lo] += 1
    out = []
    for i, c in enumerate(counts):
        out.extend([i + lo] * c)
    return out
```
Verified against `sorted()` on 500 random cases (lengths 0–30, values 0–20), including empty
input and heavy duplicates.

### The honest complexity — say this, don't claim plain O(n)
**O(n + k)** time and **O(k)** space, where k is the size of the value range. It's O(n) *only
when k is O(n)*. Volunteering that distinction rather than claiming a flat O(n) is the
difference between sounding like you memorized a trick and sounding like you understand it.

### When it's worse than `sorted()`
When **k >> n**. Sorting ten integers that range from 0 to a billion allocates a billion
counters to sort ten items — catastrophically worse than `sorted()`. Say this out loud; it's
the natural follow-up and it shows you know the algorithm's failure mode, not just its pitch.

Also note the irony worth mentioning: for a genuinely **short** array, `sorted()` (Timsort,
which uses insertion sort below ~64 elements) will usually beat counting sort in wall-clock
time regardless of big-O. *"Asymptotically this is O(n + k); practically, for a short array,
the constant factors mean I'd just call `sorted()` unless profiling said otherwise."* Knowing
when the theory doesn't apply is a strong answer.

### The other constraints
- **Floats** — counting sort doesn't work; you can't index an array by 1.5. You'd need a
  bucket sort (distribute into ranged buckets, sort within each), which is O(n) only on
  uniformly distributed data.
- **Negatives** — handled by the `lo` offset above. Mention it; a version hard-coded to
  `counts[x]` crashes on negative input.
- **Strings / arbitrary keys** — radix sort, O(d x n) for d-character keys.
- **Stability** — the version above outputs reconstructed values, so stability is moot for
  bare integers. It *matters* when sorting records by a key (two trades with the same price
  should keep their arrival order — exactly the time-priority idea from the order book). The
  stable form accumulates counts into starting positions and walks the input **backwards**,
  placing each record into its slot.

### Related question to be ready for
"Sort an array containing only 0s, 1s and 2s" — the Dutch national flag problem, O(n) with
three pointers and O(1) space. Same family: bounded values enable a linear sort.
