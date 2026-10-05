# Solutions — Drill Set 4 (Control Flow and Functions)

## 1. FizzBuzz
```python
def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
```
**Order matters**: check "divisible by both" *first*. If you check `% 3` before `% 15` cases
separately, a number like 15 would hit the `Fizz` branch and never reach a `FizzBuzz` check.
`range(1, n + 1)` because we want 1 through `n` inclusive, and `range`'s stop is exclusive.

## 2. Is prime
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
```
1 and numbers below are not prime by definition — handle that explicitly first. Then check
every number from 2 up to (but not including) `n` itself; if any divides evenly, it's not
prime. (An optimization — only check up to `n**0.5` — is good to *mention* if asked "can
this be faster", but the simple version above is correct and is a perfectly fine first
answer.)

## 3. Fibonacci
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```
`a, b = b, a + b` is simultaneous assignment — both right-hand values are computed *before*
either variable is updated, so this correctly means "a becomes the old b, b becomes the sum
of the old a and old b" without needing a temporary variable. Trace it by hand for n=6:
starts (0,1) -> (1,1) -> (1,2) -> (2,3) -> (3,5) -> (5,8) -> (8,13), loop runs 6 times,
returns `a = 8`. `_` is conventional for "loop variable I don't actually use".

## 4. Validate a simple password
```python
def is_valid_password(s):
    if len(s) < 8:
        return False
    has_digit = any(ch.isdigit() for ch in s)
    has_upper = any(ch.isupper() for ch in s)
    return has_digit and has_upper
```
`any(...)` returns `True` if at least one element of the generator is truthy — a clean way
to express "does at least one character satisfy this condition" without manually tracking a
boolean flag through a loop. The manual-loop equivalent, if `any()` with a generator feels
unfamiliar:
```python
has_digit = False
for ch in s:
    if ch.isdigit():
        has_digit = True
```

## 5. Greatest common divisor
```python
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
```
Same simultaneous-assignment trick as Fibonacci. Trace `gcd(48, 18)`: (48,18) -> (18, 48%18=12)
-> (12, 18%12=6) -> (6, 12%6=0) -> loop stops since b==0, return `a = 6`. Recursive version,
if that's more natural to reach for: `return a if b == 0 else gcd(b, a % b)`.

## 6. Apply a function n times
```python
def repeat(f, x, n):
    for _ in range(n):
        x = f(x)
    return x
```
Functions are values in Python — `f` can be passed around and called like any other
variable holding a callable. Each iteration reassigns `x` to the result of calling `f` on
the *current* `x`, chaining the applications.
