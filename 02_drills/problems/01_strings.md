# Drill Set 1 — Strings

Solve each without looking at `../solutions/01_strings.md`.

## 1. Reverse a string
Write `reverse(s)` that returns the string reversed.
```
reverse("hello") -> "olleh"
```

## 2. Is palindrome
Write `is_palindrome(s)` that returns `True` if `s` reads the same forwards and backwards,
`False` otherwise. Treat it as case-sensitive for now (no need to handle spaces/punctuation).
```
is_palindrome("racecar") -> True
is_palindrome("hello")   -> False
```

## 3. Count vowels
Write `count_vowels(s)` that returns the number of vowels (a, e, i, o, u — either case) in
`s`.
```
count_vowels("Hello World") -> 3
```

## 4. Word count
Write `word_count(s)` that returns the number of words in `s`, where words are separated by
whitespace (there may be multiple spaces between words, or leading/trailing spaces).
```
word_count("  the quick  brown fox ") -> 4
```

## 5. First non-repeating character
Write `first_unique_char(s)` that returns the first character in `s` that appears exactly
once. Return `None` if there isn't one.
```
first_unique_char("swiss") -> "w"
first_unique_char("aabb")  -> None
```

## 6. Caesar cipher
Write `caesar_shift(s, n)` that shifts every lowercase letter in `s` forward by `n` positions
in the alphabet, wrapping around from 'z' back to 'a'. You can assume `s` is all lowercase
letters and spaces, and spaces are left unchanged. (Hint: `ord()` gives you a character's
numeric code, `chr()` goes the other way.)
```
caesar_shift("abc xyz", 2) -> "cde zab"
```
