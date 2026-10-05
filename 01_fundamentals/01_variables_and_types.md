# Variables and Types

## Declaring variables
No type keyword needed — the value determines the type.

```python
x = 5          # int
y = 3.45       # float
name = "Nick"  # str
flag = True    # bool
nothing = None # the "no value" value
```

`print(x)` shows the value. `type(x)` shows the type — use this constantly when you're unsure
what you're holding.

## The core types you'll actually use
| Type | Example | Notes |
|---|---|---|
| `int` | `5`, `-3` | whole numbers |
| `float` | `3.45` | decimals |
| `str` | `"hi"` | text, immutable |
| `bool` | `True`/`False` | capitalized! |
| `list` | `[1, 2, 3]` | ordered, mutable |
| `dict` | `{"a": 1}` | key → value |
| `None` | `None` | absence of a value |

## Type conversion
```python
int("5")      # 5
float("5")    # 5.0
str(5)        # "5"
bool(1)       # True
bool(0)       # False
```
This comes up constantly when reading input, since raw input is always a string.

## Arithmetic operators
```python
5 + 2   # 7
5 - 2   # 3
5 * 2   # 10
5 / 2   # 2.5   <- true division, ALWAYS returns a float
5 // 2  # 2     <- floor (integer) division
5 % 2   # 1     <- remainder / modulo
5 ** 2  # 25    <- exponent
```
**Gotcha:** `/` always gives a float in Python 3, even `4 / 2` gives `2.0`. If you need an
integer result, use `//`. This distinction trips people up under time pressure — know it cold.

## Truthiness (very high leverage, shows up everywhere)
In an `if` condition, these values count as **falsy**: `0`, `0.0`, `""` (empty string),
`[]` (empty list), `{}` (empty dict), `set()` (empty set), and `None`. Everything else is
truthy. This means:

```python
my_list = []
if my_list:
    print("has items")
else:
    print("empty")   # this runs
```

You'll use this constantly to check "is this list/string/dict empty" without writing
`len(my_list) == 0`.

## Mutability (preview — matters a lot for lists/dicts later)
`int`, `float`, `str`, `bool`, `tuple` are **immutable** — you can't change them in place,
only reassign the variable to a new value. `list`, `dict`, `set` are **mutable** — you can
change their contents without reassigning. This distinction is the source of a very common
bug (see `03_lists_and_tuples.md` → aliasing).

## Comparison vs assignment
`=` assigns. `==` compares equality. Mixing these up is a classic slip under pressure —
say the code out loud as you write it ("if num equals equals five") to catch it.
