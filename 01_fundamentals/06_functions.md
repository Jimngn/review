# Functions

## Defining and calling
```python
def add(a, b):
    return a + b

result = add(3, 4)   # 7
```
`def`, name, parenthesized parameters, colon, indented body, `return`. `return` immediately
exits the function — code after it in the same branch never runs.

A function with no `return` statement returns `None` implicitly. This is a common source of
confusion when you forget to `return` and then try to use the result.

## Default arguments
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Nick")                 # "Hello, Nick!"
greet("Nick", "Hi")            # "Hi, Nick!"
greet("Nick", greeting="Yo")   # "Yo, Nick!"  <- keyword argument, order doesn't matter
```

## Returning multiple values
Python lets you return a tuple and unpack it at the call site — this is how you "return two
things" without a special construct:
```python
def stats(nums):
    return min(nums), max(nums), sum(nums)

lo, hi, total = stats([3, 1, 4, 1, 5])
```

## Scope (the part that bites people)
Variables created inside a function are **local** — they don't exist outside it, and they
don't clash with a same-named variable outside.
```python
x = 10
def foo():
    x = 20      # this is a NEW local x, doesn't touch the outer one
    return x

foo()      # 20
print(x)   # 10, unchanged
```
A function *can read* an outer/global variable if it doesn't assign to a variable of the
same name inside itself — but relying on that is a common source of bugs. Prefer passing
values in as parameters and getting results out via `return`, rather than reading/mutating
variables from an outer scope. It makes the function's behavior obvious from its signature
alone, which matters a lot when you're being watched write it live.

## Recursion — know the shape, don't need much beyond this
A function that calls itself, with a **base case** that stops the recursion.
```python
def factorial(n):
    if n <= 1:              # base case — without this, infinite recursion -> crash
        return 1
    return n * factorial(n - 1)   # recursive case: solve a smaller version of the problem
```
Ask yourself two questions for any recursive function: (1) what's the smallest input I can
answer directly (base case)? (2) how do I express the answer for input `n` in terms of the
answer for a smaller input? If you can answer both, you can write the function. Most
practical-interview problems can also be solved with a plain loop — if recursion isn't
clicking under pressure, reach for a loop instead; it's rarely the wrong choice for a
practical (non-algorithms-focused) problem.

## Writing functions during an interview: practical advice
- Give the function and its parameters honest, descriptive names (`find_max`, not `f`) —
  it costs nothing and makes your own code easier to reason about out loud.
- Handle the obvious edge case (empty list, zero, empty string) either by an explicit check
  at the top, or by tracing through what your loop naturally does with that input — and say
  out loud which one you're relying on.
- Test it yourself before saying "done": call it with a small example and a trivial/edge
  example, and read the output line by line.
