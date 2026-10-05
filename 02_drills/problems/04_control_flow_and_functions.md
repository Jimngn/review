# Drill Set 4 — Control Flow and Functions

Solve each without looking at `../solutions/04_control_flow_and_functions.md`.

## 1. FizzBuzz
Write `fizzbuzz(n)` that returns a list of strings for numbers 1 through `n`: `"Fizz"` for
multiples of 3, `"Buzz"` for multiples of 5, `"FizzBuzz"` for multiples of both, otherwise
the number itself as a string.
```
fizzbuzz(15) -> ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]
```

## 2. Is prime
Write `is_prime(n)` that returns whether `n` is a prime number. Assume `n` is a positive
integer.
```
is_prime(7) -> True
is_prime(8) -> False
is_prime(1) -> False
```

## 3. Fibonacci
Write `fibonacci(n)` that returns the `n`th Fibonacci number (0-indexed: `fibonacci(0) == 0`,
`fibonacci(1) == 1`). Do it with a loop, not recursion (recursion works but is much slower
for this without extra machinery).
```
fibonacci(0) -> 0
fibonacci(1) -> 1
fibonacci(6) -> 8
```

## 4. Validate a simple password
Write `is_valid_password(s)` that returns `True` if `s` is at least 8 characters long,
contains at least one digit, and contains at least one uppercase letter. Otherwise `False`.
```
is_valid_password("Abcdefg1") -> True
is_valid_password("abcdefg1") -> False   # no uppercase
is_valid_password("Abc1")     -> False   # too short
```

## 5. Greatest common divisor
Write `gcd(a, b)` that returns the greatest common divisor of two positive integers, using
Euclid's algorithm (`gcd(a, b) == gcd(b, a % b)`, with `gcd(a, 0) == a`).
```
gcd(48, 18) -> 6
```

## 6. Apply a function n times
Write `repeat(f, x, n)` that applies function `f` to `x`, `n` times in a row, and returns the
final result.
```
repeat(lambda x: x * 2, 3, 4) -> 48    # 3 -> 6 -> 12 -> 24 -> 48
```
