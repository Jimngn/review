# Answers 4: Practice set (Q20–Q27)

Questions: [../questions/04_practice_set.md](../questions/04_practice_set.md)

⚠️ = a question or follow-up that has an error or can't be solved as stated. Your original notes got some of
these wrong, and each is a good moment to ask a clarifying question.

---

## Q20. Die: keep or reroll

**Answer: Keep 4–6 and reroll 1–3. The game is worth 4.25.**

- **Q20.1 — 14/3 ≈ 4.67.** Keep 5+ on the first roll (see Q14.2).
- **Q20.2 — Keep 11–20. The game is worth 13.** Keep if the roll beats (n+1)/2 = 10.5. ½·15.5 + ½·10.5 = 13.
- **Q20.3 — Keep 3 or higher. The game is worth 23/6 ≈ 3.83.** A reroll is worth 3.5 − 1 = 2.5. (4/6)·4.5 + (2/6)·2.5.
- **Q20.4 — Same answer.** A threshold strategy is already optimal. **Say why:** the decision depends only on the
  current roll compared with the value of continuing, and you know both of those in advance.

---

## Q21. Three coins

**Answer: 3/8.**

- **Q21.1 — 1/2.**
- **Q21.2 — 3p²(1−p).**
- **Q21.3 — 6.** See Q15.2 for the state equations.
- **Q21.4 — 1/p.**

---

## Q22. Meeting at a coffee shop

**Answer: 5/9.** 1 − (40/60)².

- **Q22.1 — 31/72 ≈ 0.43.** They miss if B arrives more than 10 min after A (a triangle with legs 50) or A arrives
  more than 20 min after B (legs 40). 1 − (1250 + 800)/3600.
- ⚠️ **Q22.2 — Yes, it changes.** Only w/T matters, and it drops from 1/3 to 1/6: 1 − (5/6)² = **11/36 ≈ 0.31**.
  The answer only stays 5/9 if the wait also doubles. (Your original notes got this wrong.)
- **Q22.3 — 7/27 ≈ 0.26.** You need (last arrival − first arrival) ≤ 20, so d = 1/3. P(range ≤ d) = 3d² − 2d³.
- **Q22.4 —** Draw random pairs of arrival times and count the fraction with |x − y| ≤ 20. The standard error is
  √(p(1−p)/N) ≈ 0.5/√N, so **10,000 samples gets you within about ±0.005.**

---

## Q23. Bus passengers

⚠️ **Answer: impossible as stated.** Work backward: 20 − 5 = 15 = (2/3)·x, so x = **22.5**. That isn't a whole
number. Saying this out loud is exactly the "integer constraint" twist they're testing.
- Fixed version (ending with 21): 21 − 5 = 16 = (2/3)·24 → 24 − 3 = 21 = half of **42**.
  Check: 42 → 21 + 3 = 24 → 24 − 8 + 5 = 21 ✓.

- **Q23.1 — The start must be ≡ 0 (mod 6).** It has to be even (to halve it), and start/2 + 3 must be divisible
  by 3 (to take a third).
- **Q23.2 —** Write each stop as xₖ₊₁ = aₖ·xₖ + bₖ, invert it step by step, and check that every intermediate
  value is a whole number.

---

## Q24. Date with all digits different

**Answer: 17/06/2345.**
- The day starts with 0–3 and the month starts with 0 or 1, so the day and month together have to use
  **both 0 and 1**. (If they didn't, the year would have to avoid 2, pushing it past 3000.)
- So the year can't use 0 or 1, and the smallest possible year is **2345**. Years 20xx, 21xx, and 22xx all fail.
  Say why.
- The month and day have to come from {0, 1, 6, 7, 8, 9}: month **06**, day **17**.

- **Q24.1 — Same answer.** The digits are the same, only the order differs. It shows you understand the method.
- **Q24.2 — +5 or +6 days.** See Q13d.
- **Q24.3 — Set it up:** count the valid (day, month) pairs with distinct digits, and for each one count the years
  whose 4 digits avoid those digits and each other. Divide by the total number of dates. You don't need to finish it.

---

## Q25. Two children

**Answer: 1/3.**

- **Q25.1 — 1/2.**
- **Q25.2 — 13/27.** Of the 14 × 14 equally likely (sex, weekday) pairs, 14² − 13² = 27 include a Tuesday boy,
  and 13 of those are two boys.
- **Q25.3 — 1/7.** Of the 7 equally likely outcomes with at least one boy, only BBB is all boys.

---

## Q26. Matching coins with a partner

⚠️ **As stated, there's no decision to make.** P(match) = p² + (1−p)², which is ≥ ½. **Ask what you actually control.**
If you can choose which side to show, agree beforehand on "both show heads" → **100%**.

- **Q26.1 —** You still can't do better than a rule agreed in advance. With random flips, P(match) ≥ ½ no matter
  what p is.
- **Q26.2 — Binomial(100, p² + (1−p)²).** Your strategy changes each game's win probability, and the law of large
  numbers makes the total predictable.

---

## Q27. Strawberry and mixtures

**Answer: 4 g.** The dry mass is 2 g, and it's now 50% of the total.

- **Q27.1 — 20 g.** 2 / 0.10.
- **Q27.2 — Add about 8.9 g.** The water stays at 98 g, which becomes 90% of the new total → 108.9 g → the dry mass goes from 2 g to 10.9 g.
