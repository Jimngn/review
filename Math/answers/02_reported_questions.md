# Answers 2: Reported by other TDO/TDOE candidates (Q6–Q13)

Questions: [../questions/02_reported_questions.md](../questions/02_reported_questions.md)

---

## Q6. Strawberry water content

**Answer: 50 g.** The dry part stays at 1 g. It's now 2% of the total, so the total is 1 / 0.02 = 50 g.

- **Q6.1 — Drain 0.96 g.** Dry part = 0.02 g, which will be 50% of the total. The new total is 0.04 g.
- **Q6.2 — The weight scales by 4/5.** The dry part (40%) becomes 50%. In general, new weight = W·(1−a)/(1−b),
  going from fraction a of water to fraction b.
- **Q6.3 —** Drying only removes water. Nothing adds or removes solids, so the dry mass is conserved. Every
  fraction problem like this comes down to finding the quantity that doesn't change. They push on this.

---

## Q7. Fewest bills

**Answer: 7 bills.** Use powers of 2 (1, 2, 4, 8, 16, 32 cover 1–63) plus one bill between $37 and $64.
- **Why 7 is the minimum:** 6 bills give only 2⁶ − 1 = 63 non-empty subsets, which can't cover 100 amounts.

- **Q7.1 — 8 bills**, for example {1, 2, 2, 5} + {10, 20, 20, 50}.
  - Amounts $1–$9 can only use bills under $10, and 3 bills give only 7 non-empty subsets, so you need 4 small bills.
  - Minimality: with 7 bills (4 small + 3 big), the small bills cover at most 0–10 (11 values). 3 big bills
    give 8 subsets, and 8 × 11 = 88 < 101 values (0–100). Using more small bills and fewer big ones is even
    worse. (A brute-force search confirms 8.)
  - Other optimal sets: {1, 1, 2, 5, 10, 20, 20, 50} and {1, 2, 2, 5, 10, 10, 20, 50}.
- **Q7.2 — ⌈log₂(N+1)⌉ bills** with free denominations. Each bill doubles the number of reachable subsets.
- **Q7.3 — Clarify first. It's a different problem.**
  - If the other side has unlimited change, one $100 bill covers everything.
  - If change can only come in the same denominations you carry (like the balance-scale weights puzzle),
    powers of 3 work: {1, 3, 9, 27, 81} covers 1–121 with **5 bills** (balanced ternary).

---

## Q8. Coins and counting

**Answer: 5/16.** C(5,3)/32 = 10/32.

- **Q8.1 — 1/2.** (10 + 5 + 1)/32, or by symmetry: "≥ 3 heads" and "≥ 3 tails" split the outcomes evenly.
- **Q8.2 — 1/2.**
- **Q8.3 — Still 1/2.** A single fair coin makes the parity 50/50, whatever the other coins do.
- **Q8.4 — 26³ = 17,576.** The first 3 letters determine the rest.
- **Q8.5 — 26³.** The first 3 letters still determine the rest.
- **Q8.6 — 26·25·24 = 15,600.**

---

## Q9. Sums of consecutive integers

**Answer: 975.**
- A sum of 2 consecutive integers is 2k + 1, which is odd. A sum of 3 is 3k + 3, a multiple of 3. A sum of 5 is
  5k + 10, a multiple of 5.
- So you need an **odd multiple of 15**. 990 is even, which gives 975.

- **Q9.1 — Impossible.** A sum of 4 consecutive integers is 4k + 6 ≡ 2 (mod 4), which is even. That
  conflicts with "odd".

---

## Q10. Digit products

**Answer: 268.** No 2-digit number works, because the maximum product is 9·9 = 81. The 3-digit options are
{2,6,8}, {3,4,8}, {4,4,6}, and the smallest arrangement is 268.

- **Q10.1 — Clarify: it's unbounded if 1s are allowed** (2681, 26811, …). Point that out.
  - Without 1s: use as many digits as possible. 96 = 2⁵·3, so use six digits {3,2,2,2,2,2} → **322222**.

---

## Q11. Two people meeting

**Answer: 5/9.** Draw the 60×60 square. They miss when |x − y| > 20, which is two triangles with legs 40.
1 − (40/60)² = 5/9.

- **Q11.1 — 1 − (1 − w/T)².** Only the ratio w/T matters.
- **Q11.2 — The square minus two unequal triangles.** With waits w₁ and w₂, the legs are T − w₁ and T − w₂:
  P = 1 − [(T−w₁)² + (T−w₂)²] / (2T²). See Q22.1 for a worked example.

---

## Q12. Train vs. walking

**Answer: a tie in expectation.** Train: E[wait] = 5, plus a 5-min ride, gives 10. Walking takes 10.
**Walking has zero variance**, so it wins if you care about risk at all.

- **Q12.1 — Walk.** Walking arrives in 10 minutes for sure. The train arrives within 12 only if the wait is
  ≤ 7, which is 70%.
- **Q12.2 — Walk.** The train now takes 2 + 5 + 5 = 12 in expectation vs. 10.
- **Q12.3 — Walk.** Poisson means E[wait] = 10 (memoryless), so the train takes 15 in expectation.
- **Q12.4 — Take the train iff the next one is less than 5 minutes away.** Expected time =
  ½·7.5 + ½·10 = **8.75**, so the information is worth **1.25 min** on average.
- Expect them to keep adding factors: timetable uncertainty, late trains, variance vs. mean. For each one,
  say what changed first, then compute.

---

## Q13. Rapid fire

- **Q13a — 75%.** 1 − 0.5² = 0.75.
  - **Q13a.1 —** You need P(both). P(at least one) = P(Sat) + P(Sun) − P(both). **Positive correlation raises
    P(both) and lowers the answer.** For example, P(rain Sun | rain Sat) = 0.8 gives 1 − 0.4 = 60%. The answer
    ranges from 50% (perfectly correlated) to 100% (perfectly anti-correlated).
- **Q13b — 1/221.** (4/52)(3/51).
- **Q13c — 105°.** The hour hand is at 270 + 15 = 285°, and the minute hand is at 180°.
  - **Q13c.1 — |30H − 5.5M|**, and take 360 minus that if it's over 180.
- **Q13d — +5 or +6 days.** 3650 ≡ 3 (mod 7), plus 2 or 3 leap days, depending on where the Feb 29s fall.
