# Lists and Tuples

## Lists — your default "collection of things"
```python
nums = [1, 2, 3, 4, 5]
mixed = ["Nick", 3.0, True]     # mixing types is allowed but unusual in practice
empty = []                      # or list()
```

### Indexing and slicing — identical rules to strings
```python
nums[0]      # 1
nums[-1]     # 5
nums[1:3]    # [2, 3]
nums[:2]     # [1, 2]
nums[2:]     # [3, 4, 5]
len(nums)    # 5
```

### Built-in aggregate functions (numbers only, except len)
```python
max(nums)   # 5
min(nums)   # 1
sum(nums)   # 15
len(nums)   # 5
sorted(nums)             # returns a NEW sorted list, ascending
sorted(nums, reverse=True)
```

### Mutating methods (change the list in place, most return `None`)
```python
nums.append(6)        # add to end
nums.insert(0, 99)     # insert at index 0
nums.remove(99)        # remove FIRST occurrence of value 99 (raises if not found)
del nums[0]             # remove by index
popped = nums.pop()     # removes AND returns last element (or nums.pop(i) for index i)
nums.sort()             # sorts in place, returns None — don't write `nums = nums.sort()`
nums.reverse()          # reverses in place
nums.index(3)           # index of first occurrence of value 3 (raises if not found)
3 in nums               # True/False, membership test
```
**Gotcha:** `sort()` (method, in-place, returns `None`) vs `sorted()` (function, returns a
new list). Confusing these is extremely common — `x = nums.sort()` silently sets `x` to
`None`.

### List comprehensions — the highest-leverage syntax in this file
A compact way to build a new list by transforming/filtering another one.
```python
squares = [x ** 2 for x in range(5)]          # [0, 1, 4, 9, 16]
evens = [x for x in nums if x % 2 == 0]        # filter
upper = [s.upper() for s in ["a", "b"]]        # transform strings

# Read it as: "for x in <source>, keep/transform x, if <condition>"
```
You could write the equivalent with a `for` loop and `.append()` — comprehensions are just
more idiomatic and faster to write live. If a comprehension feels shaky under pressure, the
explicit loop version is always a safe fallback and equally correct.

### `enumerate` and `zip` — used constantly in practical problems
```python
names = ["Nick", "Shreya", "Reese"]

for i, name in enumerate(names):
    print(i, name)              # 0 Nick / 1 Shreya / 2 Reese

ages = [30, 28, 25]
for name, age in zip(names, ages):
    print(name, age)            # pairs elements from both lists together
```

### Tuples — like lists, but immutable
```python
point = (3, 4)
x, y = point          # unpacking — extremely common and useful
```
Use a tuple when the collection shouldn't change (e.g., a fixed pair like coordinates) or
when you want to return multiple values from a function:
```python
def min_and_max(nums):
    return min(nums), max(nums)   # this actually returns a tuple (min, max)

lo, hi = min_and_max([3, 1, 4])   # unpack immediately
```

## The #1 list bug: aliasing vs copying
Lists are mutable, and assigning a list to a new variable does **not** copy it — both names
point at the same list in memory.
```python
a = [1, 2, 3]
b = a          # b is NOT a copy, it's the same list
b.append(4)
print(a)       # [1, 2, 3, 4]  <- a changed too! surprising if you didn't expect it

c = a[:]           # a real, independent copy (full slice)
d = list(a)        # also a real copy
```
This is the single most common "why did my data get mysteriously mutated" bug. If you pass
a list into a function and modify it there, the caller's list changes too — that's sometimes
what you want, and sometimes a bug. Be deliberate about it.
