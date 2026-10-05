# Mock 4 — No-Execution Manual Tracing

One report specifically mentioned code execution was **not allowed** in this round, and
another described **pseudocode in a shared notepad** with heavy emphasis on explaining
reasoning and catching edge cases — not typing speed. This mock trains exactly that: reading
code (including code with bugs) and reasoning about its behavior with no interpreter.

**Rule for this whole file: do not run any of this code until you've written down your full
answer by hand first.** That's the actual skill being drilled.

## Exercise 1 — find the bug
Here is a function meant to remove all negative numbers from a list, in place, by index:
```python
def remove_negatives(nums):
    for i in range(len(nums)):
        if nums[i] < 0:
            del nums[i]
    return nums
```
Trace `remove_negatives([1, -2, -3, 4])` by hand, step by step, tracking the value of `i`,
the state of `nums`, and what `nums[i]` refers to at each iteration. What does it actually
return? Is it correct? If not, why not, in your own words — and then fix it.

## Exercise 2 — find the bug
Here is a function meant to compute the average of a list of numbers:
```python
def average(nums):
    total = 0
    for i in range(1, len(nums)):
        total += nums[i]
    return total / len(nums)
```
Trace `average([10, 20, 30])` by hand. What value does it actually produce, and what should
it produce? Identify exactly which line is wrong and why.

## Exercise 3 — find the bug
Here is a function meant to build a dictionary counting how many times each word appears in
a list, then return the single most common word:
```python
def most_common_word(words):
    counts = {}
    for word in words:
        counts[word] += 1
    return max(counts, key=counts.get)
```
Trace `most_common_word(["a", "b", "a"])` by hand line by line. What actually happens when
this runs (name the specific error), and why? Fix it.

## Exercise 4 — no bug, just trace it
This one is correct — the exercise is purely reading comprehension under time pressure, the
skill that matters when you can't just run something to "see what happens":
```python
def mystery(nums):
    result = []
    seen = set()
    for x in nums:
        if x not in seen:
            result.append(x)
            seen.add(x)
    return result
```
Without running it, state in one sentence what this function computes, then trace
`mystery([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])` by hand to get the exact output.

## Exercise 5 — pseudocode from a word problem (no Python syntax needed)
On paper or in a plain text file, write **pseudocode only** (numbered steps in plain English
or loose syntax, not runnable Python) for the following, the way you might in a shared
notepad before writing real code:

> "Given a list of employee records, each with a name and a department, produce a list of
> department names that have more than one employee, sorted alphabetically."

Then state out loud: what data structure would you reach for first, and why, before writing
any real code.
