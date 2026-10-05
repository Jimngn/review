# One-Page Cheatsheet (for studying only — not for the interview itself)

## Types & conversion
```python
int("5"); float("5"); str(5); bool(0)      # 0, 0.0, "", [], {}, None are all falsy
5 / 2   # 2.5  (always float)
5 // 2  # 2    (floor div)
5 % 2   # 1
```

## Strings
```python
s[0]; s[-1]; s[1:3]; s[::-1]
s.strip(); s.lower(); s.upper()
s.split(" "); s.split(); "-".join(list_of_strs)
s.replace(old, new); s.startswith(x); "sub" in s
f"{name} is {age}"
```

## Lists
```python
lst[0]; lst[-1]; lst[1:3]
lst.append(x); lst.insert(i, x); lst.remove(value); lst.pop(); del lst[i]
lst.sort(); sorted(lst); sorted(lst, key=fn, reverse=True)
max(lst); min(lst); sum(lst); len(lst)
[expr for x in lst if cond]                 # comprehension
for i, x in enumerate(lst): ...
for a, b in zip(lst1, lst2): ...
copy = lst[:]  or  list(lst)                # real copy; `b = a` is an ALIAS, not a copy
```

## Tuples
```python
t = (1, 2)
x, y = t                                     # unpacking
def f(): return a, b                         # "multiple return"
```

## Dicts
```python
d["key"]; d.get("key", default)
d["key"] = value; del d["key"]; "key" in d
for k, v in d.items(): ...
d.get(k, 0) + 1                              # counting idiom
max(d, key=d.get)                            # key with highest value
```

## Sets
```python
s = set(); s.add(x); s.remove(x); x in s      # O(1) membership, {} is a DICT not a set
list(set(lst))                                # dedupe (order not preserved)
```

## Control flow
```python
if cond: ... elif cond2: ... else: ...
and / or / not
while cond: ...
for i in range(start, stop, step): ...        # stop is EXCLUSIVE
break; continue
```

## Functions
```python
def f(a, b=default):
    return a + b
def f(): ...       # no return -> returns None implicitly
```

## Common errors → what they mean
```
IndexError   -> index out of range (off-by-one, or empty collection)
KeyError     -> dict key doesn't exist, use .get()
TypeError    -> mixed incompatible types (str + int), or used a None result
ValueError   -> e.g. int("abc")
AttributeError -> called a method that doesn't exist on that type (wrong data structure)
```

## The move to always consider
Nested loop checking "have I seen this" or "look this up" → replace inner list scan with a
dict/set lookup.
