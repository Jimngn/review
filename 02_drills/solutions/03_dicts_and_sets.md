# Solutions — Drill Set 3 (Dicts and Sets)

## 1. Most common element
```python
def most_common(items):
    counts = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    return max(counts, key=counts.get)
```
Build the frequency dict, then `max(counts, key=counts.get)` iterates over the dict's *keys*
and picks the one where `counts.get(key)` (its count) is largest — it returns the key, `"a"`,
not the count, which is exactly what's asked for.

## 2. Anagram check
```python
def is_anagram(s1, s2):
    s1, s2 = s1.lower().replace(" ", ""), s2.lower().replace(" ", "")
    return sorted(s1) == sorted(s2)
```
Two strings are anagrams exactly when they have the same multiset of characters — sorting
both and comparing is the simplest correct way to check that. `sorted("listen")` and
`sorted("silent")` both produce `['e','i','l','n','s','t']`. A frequency-count comparison
(build a dict for each, compare the dicts) is equally valid and avoids sorting, if you
prefer that approach.

## 3. Group words by length
```python
def group_by_length(words):
    groups = {}
    for word in words:
        length = len(word)
        if length not in groups:
            groups[length] = []
        groups[length].append(word)
    return groups
```
The "grouping" pattern: check if the key exists yet, initialize an empty list on first sight,
then always append. (`collections.defaultdict(list)` removes the need for the `if`, but the
manual version needs no import and is just as correct.)

## 4. Two-sum
```python
def two_sum(nums, target):
    seen = {}   # value -> index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    return None
```
One pass. At each element `x`, ask "have I already seen the value that, added to `x`, gives
`target`?" — that value is `target - x`. If yes, we've found our pair immediately (and
`seen[complement]` gives its index). If no, record `x`'s own index for future iterations to
find. This is O(n) instead of the O(n²) nested-loop version that checks every pair — the
canonical example of "replace an inner scan with a dict lookup" from the fundamentals.

## 5. Find all duplicates
```python
def find_duplicates(items):
    seen = set()
    dupes = set()
    for x in items:
        if x in seen:
            dupes.add(x)
        seen.add(x)
    return dupes
```
`seen` tracks everything encountered so far; the moment something shows up a second time, it
goes into `dupes`. Using a set for `dupes` means an item appearing 3+ times still only shows
up once in the result, which matches the expected output shape.

## 6. Invert a dictionary
```python
def invert(d):
    result = {}
    for key, value in d.items():
        result[value] = key
    return result
```
Comprehension version: `{value: key for key, value in d.items()}`. If values weren't
guaranteed unique, later keys would silently overwrite earlier ones in the result — worth
mentioning out loud as an assumption if the interviewer doesn't state it explicitly.
