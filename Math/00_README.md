# Math / Probability / Brainteaser: Mock Practice

## Layout
```
Math/
  00_README.md                  ← this file: how to run a session
  mock_sets.md                  ← prebuilt 30-minute rounds (3 questions each)
  practice_log.md               ← record results and track what to retry
  questions/                    ← prompts only, follow-ups collapsed
  answers/                      ← same file names, same IDs
  janestreet_tdoe_math_brainteaser_prep.md   ← original all-in-one sheet (skim the night before)
```

| File (in `questions/` and `answers/`) | Covers | Priority |
|---|---|---|
| `01_round1_repeats.md` | Q1–Q5: the questions you got in round 1 | **Know 100%.** Expect variants. |
| `02_reported_questions.md` | Q6–Q13: reported by other TDO/TDOE candidates | Know well |
| `03_core_patterns.md` | Q14–Q19: EV, patterns, Bayes, linearity, ruin, Fermi | Know well |
| `04_practice_set.md` | Q20–Q27: from your notes, includes flawed questions | Know well |
| `05_extra.md` | E1–E25 | Once 01–04 are automatic |

IDs match across files: **Q4.2** in `questions/` is **Q4.2** in `answers/`.

## Setup
- **Open question files in Markdown preview** (Cmd+Shift+V, or Cmd+K V for side-by-side). In preview, the
  follow-ups stay collapsed until you click them. The raw editor shows everything.
- Keep the answer file closed. Don't open it in a split pane.
- Use a timer and paper, and **talk out loud**. Record a voice memo if you can, then listen back for long
  silences and unexplained jumps.

## Mock mode (timed, simulates the real round)
The real format is **about 3 questions, roughly 10 min each, with 1–3 follow-ups per question.**

1. Pick a set from [mock_sets.md](mock_sets.md), or pick 3 at random:
   `python3 -c "import random; print(sorted(random.sample(range(1, 28), 3)))"`
2. For each question, follow this routine:
   1. **Restate** the problem in your own words.
   2. **Ask about anything ambiguous before solving**: tie rules, whether 1s are allowed, what you actually
      control. Write your clarifying question down. The answer key says whether there was one worth asking.
   3. **Say your approach** before you compute anything.
   4. **Solve out loud.** Don't go silent for more than about 20 seconds.
   5. **Sanity-check**: a limiting case, symmetry, or a bound.
   6. **State the answer** clearly.
3. **Open follow-ups one at a time**, and only after you've said your answer to the previous one. For each
   follow-up, **first say what changed and why it matters**, then compute. In timed mode, stop after 3
   follow-ups per question.
4. After all 3 questions, open the answer files, score yourself, and log the result.

## Study mode (untimed)
Work through a whole file, including every follow-up. Add anything you miss to the retry queue in
[practice_log.md](practice_log.md).

## Partner mode
Give a friend the answers file. It works as the interviewer's script. They read the prompt, reveal the
follow-ups in order, and give a hint if you've been stuck for about a minute, the way a real interviewer would.

## Scoring
- ✅ **Clean**: correct, assumptions stated, sanity-checked, no hint needed.
- 🟡 **Shaky**: needed a hint, was slow, or skipped the clarifying question or the sanity check.
- ❌ **Missed**: wrong or stuck.

Retry ❌ in 1–2 days and 🟡 in about 4. A question is **done** after two ✅ in a row on different days.

## General follow-up patterns
- "Change one parameter" means they're testing whether you understand the method, not whether you memorized
  the answer.
- "Check that a different way": use a limiting case, symmetry, simulation logic, or a bound.
- "How confident are you?" Give an honest range. Don't overclaim.
- If they move on with no follow-up, that usually means you answered cleanly. Don't panic.

## Interview technique checklist (from reported feedback)
- Think out loud and don't go silent. Interviewers give hints when you're stuck, but only if they can follow
  your reasoning.
- Check your answers out loud ("58 is between 50 and 70 and closer to 50, which makes sense because I spend
  longer at 50").
- Ask about ambiguous rules before solving (the dice tie rule, "largest" when 1s are allowed).
- For each follow-up, first say **what changed and why it matters**, then compute.
- Be friendly. One candidate's GDPR request showed they were rejected mainly for not seeming friendly enough.
