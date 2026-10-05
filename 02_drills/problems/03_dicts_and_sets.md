# Drill Set 3 — Dicts and Sets

Solve each without looking at `../solutions/03_dicts_and_sets.md`.

## 1. Most common element
Write `most_common(items)` that returns the element that appears most often in the list.
Assume no ties.
```
most_common(["a", "b", "a", "c", "a"]) -> "a"
```

## 2. Anagram check
Write `is_anagram(s1, s2)` that returns `True` if `s1` and `s2` contain exactly the same
letters in the same quantities (ignore case), `False` otherwise.
```
is_anagram("listen", "silent") -> True
is_anagram("hello", "world")   -> False
```

## 3. Group words by length
Write `group_by_length(words)` that returns a dict mapping each length to a list of words
of that length, in original order.
```
group_by_length(["a", "bb", "cc", "ddd"]) -> {1: ["a"], 2: ["bb", "cc"], 3: ["ddd"]}
```

## 4. Two-sum
Write `two_sum(nums, target)` that returns a tuple `(i, j)` of two indices whose values add
up to `target`, or `None` if no such pair exists. Assume at most one valid pair.
```
two_sum([2, 7, 11, 15], 9) -> (0, 1)     # 2 + 7 == 9
two_sum([1, 2, 3], 100)    -> None
```
(This is a classic — try to do it in one pass with a dict of "value seen so far -> index",
rather than a nested loop checking every pair.)

## 5. Find all duplicates
Write `find_duplicates(items)` that returns a set of all values that appear more than once.
```
find_duplicates([1, 2, 3, 2, 4, 1]) -> {1, 2}
```

## 6. Invert a dictionary
Write `invert(d)` that returns a new dict with keys and values swapped. Assume all values in
`d` are unique (so the inversion is well-defined).
```
invert({"a": 1, "b": 2}) -> {1: "a", 2: "b"}
```
