# Strings

Strings are immutable sequences of characters. Every "modifying" method returns a **new**
string — it never changes the original.

## Creating
```python
s = "Hello World"
s2 = 'also fine'
multi = """
spans
multiple lines
"""
```

## Indexing and slicing (know this cold — used constantly)
```python
s = "Hello"
s[0]      # "H"          first char
s[-1]     # "o"          last char
s[-2]     # "l"          second-to-last
s[1:3]    # "el"         index 1 up to (not including) index 3
s[:3]     # "Hel"        from start
s[3:]     # "lo"         to end
s[:]      # "Hello"      full copy
s[::-1]   # "olleH"      reverse the whole string (step of -1)
```
**Rule to memorize:** `s[start:stop]` includes `start`, excludes `stop`. Off-by-one errors on
slices are one of the most common live-coding mistakes — double check boundary cases
(empty string, single character, slicing past the end which is safe and just truncates).

## The methods you'll actually reach for
```python
s = "  Hi my name is Shreya.  "

len(s)                # 26, number of characters
s.strip()             # removes leading/trailing whitespace
s.lower(), s.upper()
s.split(" ")          # -> list of words, split on the delimiter
s.split()             # no arg = split on any whitespace, collapses multiples. Most common form.
"-".join(["a","b"])   # "a-b"  <- opposite of split, joins a list into a string
s.replace("i", "I")   # replace all occurrences
s.startswith("Hi")    # bool
s.endswith(".")       # bool
"name" in s           # True/False — substring membership test
s.find("name")        # index of first match, or -1 if not found
s.count("a")          # number of occurrences
```

`split()`/`join()` is the single most useful pair for practical problems: split raw text
into pieces, process them, join back together.

## Building strings
```python
name, age = "Nick", 30

# f-strings: the standard, cleanest way. Anything in {} is executed as Python and stringified.
print(f"{name} is {age} years old")
print(f"next year: {age + 1}")

# concatenation with + requires both sides to already be strings
print(name + " is " + str(age))   # str(age) is required — can't add str + int
```
**Gotcha:** `"age: " + 5` raises `TypeError`. You must `str(5)` first, or just use an f-string
and skip the problem entirely. Prefer f-strings — fewer ways to make this mistake.

## Iterating over a string
```python
for ch in "abc":
    print(ch)
```
A string is just a sequence like a list, so `for`, `len()`, indexing, and slicing all work
the same way.

## Common practical use: character/word frequency
```python
s = "hello world"
counts = {}
for ch in s:
    counts[ch] = counts.get(ch, 0) + 1
```
See `04_dictionaries_and_sets.md` for why `.get(ch, 0)` is the idiom here.
