# Drills — how to use this folder

## Rules for drilling yourself effectively
1. **No peeking.** Open only the problem file. Don't open the matching solution file until
   you've either finished or genuinely given up after real effort.
2. **Timebox it.** ~8-12 minutes for `01`-`04` problems, ~15-20 for `05_mixed_practical.md`.
   The actual interview is time-pressured — practice under a clock.
3. **Actually run your code.** Each problem set has a `.ipynb` notebook in `problems/` —
   open it in Jupyter, VS Code, or upload to https://colab.research.google.com/. Each
   problem has a markdown cell with the prompt, a code cell with a function stub to fill
   in, and a self-check cell with `assert`s built from the prompt's examples — run it after
   writing your solution; silent output means you passed. Still test at least one edge case
   (empty input, single element) beyond what the self-check covers, since those asserts only
   check the examples given in the prompt, not every edge case.
4. **Talk out loud while you solve it**, even alone. Say what you're doing and why. This is
   an interview skill in itself, and it's not one you can practice silently.
5. **After checking the solution**, don't just read it — note *why* it differs from yours if
   it does (wrong data structure? missed edge case? syntax slip?). That's the actual
   learning event, more than getting it right the first time.

## Order
Work through `problems/01` → `05` in order — they build on each other and roughly track the
fundamentals files. `05_mixed_practical` is the closest in spirit to the real interview:
short word-problem prompts with no hint about which data structure to use.

## Files
```
problems/
  01_strings.md            + 01_strings.ipynb
  02_lists.md               + 02_lists.ipynb
  03_dicts_and_sets.md      + 03_dicts_and_sets.ipynb
  04_control_flow_and_functions.md + 04_control_flow_and_functions.ipynb
  05_mixed_practical.md     + 05_mixed_practical.ipynb
solutions/
  (same filenames as the .md problem files, full explanations — no notebook version,
   since these are meant to be read, not run)
```
The `.md` file and `.ipynb` file for a given set have identical problems — the notebook is
just the version you actually write and run code in; the `.md` is there if you'd rather read
the prompts on their own or work in plain text/a shared-notepad style (closer to the reported
CoderPad format — see `../03_mocks/`).

## If you finish everything and want more reps
Re-do `05_mixed_practical` from scratch a day later without looking at your old answers —
re-solving after time has passed is a better test of retention than moving on to new
material you'll never revisit.
