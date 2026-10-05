# Fundamentals — the 20% that covers 80% of the interview

## What this round actually is
You'll be given a **practical problem** (not a trivia question about language spec) and asked
to write working code for it, live, with no outside references. That means the bar is:

1. You can translate a word problem into code without fumbling syntax.
2. You use the *right basic tool* for the job (dict for lookup/counting, list for order,
   set for uniqueness) instead of fighting the wrong one.
3. You catch your own edge cases (empty input, duplicates, off-by-one) before being asked.
4. You can read your own error messages and fix them without panicking.

None of that requires knowing obscure standard library functions or clever one-liners.
It requires **fluency** with a small set of fundamentals. That's what this folder covers.

## Study order
1. `01_variables_and_types.md`
2. `02_strings.md`
3. `03_lists_and_tuples.md`
4. `04_dictionaries_and_sets.md`
5. `05_control_flow.md`
6. `06_functions.md`
7. `07_practical_patterns.md` — **the highest-leverage file in this folder.** This is where
   isolated syntax knowledge turns into "I can solve a word problem."
8. `08_debugging_and_complexity.md`

Then use `CHEATSHEET.md` for quick review, and move to `../02_drills/` to test yourself.

## How to actually study this (not just read it)
Reading syntax does not build fluency — typing it does. For every code block in these files:
- Type it into a real Python interpreter yourself (don't copy-paste). Use `python3` in a
  terminal, or https://colab.research.google.com/ if you don't have Python installed.
- Predict the output before you run it. Being wrong is the useful part.
- Once a file feels familiar, close it and try to write 3-4 of its examples from memory.

## What's deliberately *not* here
No sorting algorithm implementations, no graph theory, no dynamic programming, no
big-O trivia beyond "does this lookup cost O(1) or O(n)". If the interview strays into that
territory, general problem-solving skill will matter more than memorized fundamentals — but
that's not the common case, so it's not where your prep time should go.
