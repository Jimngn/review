# Solutions — Drill Set 1 (Strings)

## 1. Reverse a string
```python
def reverse(s):
    return s[::-1]
```
The `[::-1]` slice steps backward through the whole string. Alternative, if slicing syntax
isn't comfortable yet: build it with a loop (`result = ""; for ch in s: result = ch + result`).

## 2. Is palindrome
```python
def is_palindrome(s):
    return s == s[::-1]
```
Compare the string to its own reverse. Edge case check: empty string `""` -> `"" == ""` ->
`True`, which is correct (an empty string is trivially a palindrome).

## 3. Count vowels
```python
def count_vowels(s):
    vowels = set("aeiouAEIOU")
    count = 0
    for ch in s:
        if ch in vowels:
            count += 1
    return count
```
Using a `set` for `vowels` makes `ch in vowels` an O(1) check instead of scanning a string
each time — matters little at this scale but is the right habit. A list comprehension
version: `sum(1 for ch in s if ch in vowels)`.

## 4. Word count
```python
def word_count(s):
    return len(s.split())
```
`s.split()` with **no argument** splits on any run of whitespace and automatically discards
leading/trailing empties — this is exactly why plain `.split()` (not `.split(" ")`) is the
right tool here. `.split(" ")` would count the extra spaces as empty-string "words" and give
the wrong answer.

## 5. First non-repeating character
```python
def first_unique_char(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in s:
        if counts[ch] == 1:
            return ch
    return None
```
Two passes: first build a frequency count (dict idiom from `04_dictionaries_and_sets.md`),
then walk the string *in original order* again looking for the first character whose count
is 1 — the order matters, which is why we don't just look at `counts.items()` (dicts
preserve insertion order in modern Python, but re-walking the original string is clearer and
safer to reason about under pressure).

## 6. Caesar cipher
```python
def caesar_shift(s, n):
    result = ""
    for ch in s:
        if ch == " ":
            result += ch
        else:
            shifted = (ord(ch) - ord("a") + n) % 26
            result += chr(shifted + ord("a"))
    return result
```
`ord(ch) - ord("a")` maps 'a'..'z' to 0..25. Add the shift, then `% 26` wraps around past
'z'. Add `ord("a")` back and `chr(...)` to turn the number back into a letter. This
"normalize to 0-based index, do math, wrap with `%`, convert back" shape is worth
recognizing — it reappears anywhere you need wraparound behavior (clock arithmetic, circular
buffers, etc).
