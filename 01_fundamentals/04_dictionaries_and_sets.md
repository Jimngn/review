# Dictionaries and Sets

These two data structures, used well, solve a huge fraction of practical interview problems.
If a problem involves "counting", "looking things up fast", or "checking for duplicates" —
reach here first, before reaching for nested loops.

## Dictionaries — key → value lookup
```python
years = {"freshman": 9, "sophomore": 10}

years["freshman"]          # 9
years["junior"] = 11        # add/overwrite a key
del years["junior"]         # remove a key

"freshman" in years         # True  <- membership check is on KEYS, and it's fast (O(1))
"freshman" in years.keys()  # same thing, more explicit
```

**Gotcha:** `years["nope"]` raises `KeyError` if the key doesn't exist. Use `.get()` to avoid
crashing:
```python
years.get("nope")          # None, no crash
years.get("nope", 0)       # 0, your own default instead of None
```

### Iterating
```python
for key in years:                  # iterates over keys by default
    print(key)

for key, value in years.items():   # the one you'll use most
    print(key, value)

for value in years.values():
    print(value)
```

### The counting idiom — extremely common in practical problems
```python
words = ["a", "b", "a", "c", "b", "a"]
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
# counts = {"a": 3, "b": 2, "c": 1}
```
Read `.get(w, 0)` as "current count for w, or 0 if we haven't seen it yet". This pattern
(dict as an accumulator inside a loop) is worth being able to write from muscle memory.

There's also `collections.Counter` which does this in one line (`Counter(words)`), and
`collections.defaultdict(int)` which auto-initializes missing keys to 0 — both fine to use
if you remember the import, but the manual `.get()` version above works with zero imports
and zero risk of forgetting the exact API, so it's the safer default under interview pressure.

### Grouping — the other extremely common dict pattern
```python
names = ["Amy", "Bob", "Ann", "Ben"]
by_first_letter = {}
for name in names:
    key = name[0]
    if key not in by_first_letter:
        by_first_letter[key] = []
    by_first_letter[key].append(name)
# {"A": ["Amy", "Ann"], "B": ["Bob", "Ben"]}
```
Same shape as counting, but the value is a list you're appending to instead of a number
you're incrementing.

## Sets — unordered collection of unique values, fast membership testing
```python
s = {1, 2, 3}
empty_set = set()          # NOT {} — that makes an empty dict!

s.add(4)
s.remove(2)                 # raises if not present
2 in s                       # fast (O(1)) membership check, same idea as dict keys

# dedupe a list while losing order:
unique = list(set([1, 2, 2, 3, 3, 3]))    # [1, 2, 3] in some order

# set algebra, occasionally useful:
a, b = {1, 2, 3}, {2, 3, 4}
a & b     # intersection {2, 3}
a | b     # union {1, 2, 3, 4}
a - b     # difference {1}
```
**Gotcha:** `{}` is an empty **dict**, not an empty set. Use `set()` for an empty set.

## Why this matters: the O(1) vs O(n) intuition
Checking `x in some_list` scans the whole list in the worst case — slow for large lists.
Checking `x in some_dict` or `x in some_set` is (effectively) instant regardless of size,
because of hashing. If you catch yourself writing a nested loop to check "have I seen this
before", stop and ask whether a set solves it in one pass instead. This single substitution
is one of the most common "make your solution actually good" moves in a practical interview.
```python
# O(n^2)-ish: nested loop to find duplicates
seen = []
dupes = []
for x in items:
    if x in seen:          # scans `seen` every time
        dupes.append(x)
    seen.append(x)

# O(n): same logic, set instead of list
seen = set()
dupes = []
for x in items:
    if x in seen:          # O(1) check
        dupes.append(x)
    seen.add(x)
```
