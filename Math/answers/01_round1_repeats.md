# Answers 1: What you were asked in round 1 (Q1–Q5)

Questions: [../questions/01_round1_repeats.md](../questions/01_round1_repeats.md)

In the interview, **say your assumptions out loud, check your answer against a sanity bound, and treat
each follow-up as the real question.**

---

## Q1. Rollercoaster average speed

**Answer: 58.33 mph.** Total distance / total time = 2 / (1/70 + 1/50) = 700/12. This is the harmonic
mean, not 60.
- **Trap:** 60 is wrong because you spend more *time* at the slower speed.
- **Sanity check:** it's between 50 and 70 and closer to 50, which makes sense because more of the time is spent at 50.

- **Q1.1 — 52.5 mph.** 2/(1/70 + 1/v) = 60, so 1/v = 1/30 − 1/70 = 4/210.
- **Q1.2 — No.** Averaging 70 over 2 miles needs a total time of 2/70 = 1/35 hr. Loop 1 at 35 mph already
  takes 1/35 hr, so loop 2 would need infinite speed.
- **Q1.3 — When you spend equal *time* (not equal distance) at each speed.**
- **Q1.4 — The harmonic mean, n / Σ(1/vᵢ).** It's always ≤ the arithmetic mean, with equality only when all
  the speeds are equal.

---

## Q2. Dice vs. two other players

**Ask first: what triggers a reroll?** Is it any tie for the top (Rule B), or only a tie that includes you
(Rule A)? Also confirm that a reroll means all three roll again.

**Answer: 1/3** by symmetry. Rerolls don't break the symmetry.

- **Q2.1 — The rule changes the answer. Pointing that out is the insight they're looking for.**
  - Rule A (reroll only if you tie for the top): you win on a 5 or 6 (2/6). A 4 makes a 3-way tie, so
    everyone rerolls and you get 1/3. A 1–3 loses. P = 2/6 + (1/6)(1/3) = **7/18 ≈ 0.389**.
  - Rule B (any tie for the top): if you roll 1–3, the other two are tied at the top, so everyone rerolls
    and you get 1/3. P = 2/6 + (4/6)(1/3) = **5/9 ≈ 0.556**.
- **Q2.2 — Rule A: 11/36 ≈ 0.306. Rule B: exactly 1/3.** Let Z be the other opponent's roll.
  - You roll 5: win if Z ≤ 4 (4/6), reroll if Z = 5 (1/6). You roll 6: win if Z ≤ 5 (5/6), reroll if Z = 6 (1/6).
    You roll 4: reroll if Z ≤ 4 (4/6). You roll 1–3: lose.
  - Rule A: P = (1/6)·[(4/6 + 1/18) + (5/6 + 1/18) + 4/18] = (1/6)(11/6) = **11/36**.
  - Rule B also rerolls when you roll 1–3 and Z = 4 (the two opponents tie). That adds 3·(1/6)(1/6)(1/3) = 1/36, giving **12/36 = 1/3**.
  - If a reroll only involves the tied players (so a 2-way tie is worth 1/2), the numbers change again.
    Say that you're assuming everyone rerolls.
- **Q2.3 — 1/n** by symmetry.
- **Q2.4 — Play iff P(win | your roll r) · Y > X.** Compute P(win | r):
  - Rule A: P = ((r−1)/6)² + [(r/6)² − ((r−1)/6)²]·(1/3). The first term is "both opponents lower"; the second is "you're tied for the top, then reroll".
  - | r | 1 | 2 | 3 | 4 | 5 | 6 |
    |---|---|---|---|---|---|---|
    | Rule A | 1/108 ≈ .01 | 1/18 ≈ .06 | 17/108 ≈ .16 | 17/54 ≈ .31 | 19/36 ≈ .53 | 43/54 ≈ .80 |
    | Rule B | 1/18 ≈ .06 | 5/54 ≈ .09 | 5/27 ≈ .19 | 1/3 | 29/54 ≈ .54 | 43/54 ≈ .80 |
  - Example: X = 1, Y = 2 (a double-your-money bet). Play on a 5 or 6 only.
- **Q2.5 — 5/9.** (6·5·4)/216 = 120/216.
- **Q2.6 — 119/24 ≈ 4.96.** E[max] = Σₖ P(max ≥ k) = Σₖ [1 − ((k−1)/6)³] = 6 − 225/216.

---

## Q3. The 100th digit

**Answer: 5.** 1–9 use 9 digits, which leaves 91. The two-digit numbers 10–54 (45 of them) use 90 digits,
so digit 99 is the last digit of "54". Digit 100 is the first digit of 55.

- **Q3.1 — 3.** 9 + 180 = 189 digits get you through 99. 1000 − 189 = 811 = 270·3 + 1. The numbers
  100–369 end at digit 999, so digit 1000 is the first digit of 370.
- **Q3.2 — 192.** 9 + 180 + 3.
- **Q3.3 — 21.** 10 in the ones place (1, 11, …, 91), 10 in the tens place (10–19), and 1 in 100.
- **Q3.4 — 901.** In 00–99, each digit appears 20 times: 45·20 = 900. Add 1 for 100.
- **Q3.5 — 11.** 9 from 10, 20, …, 90, plus 2 from 100.

---

## Q4. Bus: run or walk?

**Answer: 10 minutes either way.** With no information, your arrival point in the 20-minute cycle is
uniform, so the expected wait is 20/2.

- **Q4.1 — Run: 5 + 10 = 15. Walk: 10 + 10 = 20.**
  - Check: running only matters if the bus arrives 5–10 min from now (probability 5/20 = 1/4). Then running
    saves a full 20 min. 1/4 × 20 = 5 ✓.
- **Q4.2 — Run only when 5 ≤ τ < 10**, where τ = minutes until the next bus.
  - τ < 5: you miss it either way and board at τ + 20. Indifferent, so walk.
  - 5 ≤ τ < 10: running catches it. Walking means waiting 20 more minutes.
  - τ ≥ 10: you catch the same bus either way. Indifferent, so walk.
- **Q4.3 — No change.** Running only helps when it gets you onto an *earlier bus*. Otherwise you just
  trade walking time for waiting time.
- **Q4.4 —** Known schedule: run iff 5 ≤ τ < 10 **and c < 20**. Unknown schedule: the expected saving is
  5 min, so run iff **c < 5**.
- **Q4.5 — 20 minutes** (memoryless). This is the **inspection paradox**: you're more likely to arrive
  during a long gap.
- **Q4.6 — E[X²] / (2·E[X])**, which is ≥ E[X]/2, with equality only when the gaps are constant.
- **Q4.7 — Fixed schedule: 20. Poisson: still 20** (memoryless).

---

## Q5. Hiring a CEO

**Answer: Skip the first candidate, then hire the first one better than everyone you've seen. P(best) = 1/2.**
This is optimal for n = 3. Compare that with hiring the first candidate: 1/3.
- Check all 6 orders (1 = best): 123✗ 132✗ 213✓ 231✓ 312✓ 321✗ → 3/6.
- Outcomes: best 1/2, second-best 1/3, worst 1/6.

- **Q5.1 — Hire the first competent one. P = 1 − (1−p)³.** The order doesn't change the success probability.
- **Q5.2 — Skip-1 wins.**
  - The best candidate is competent if at least 1 is; the second-best if at least 2 are; the worst only if all 3 are.
  - Skip-1: P = ½[1 − (1−p)³] + ⅓[3p² − 2p³] + ⅙p³. Hire-first: P = p.
  - For example, p = 0.9 gives ≈ 0.945 vs. 0.90. **Say why:** being best-so-far is correlated with being competent.
- **Q5.3 — Not for success, only for cost.** If you stop at the first competent one, P(success) =
  1 − 0.3·0.5·0.7 = **0.895** in *any* order. Order still matters for **cost and time**: interview A, then B,
  then C to minimize the expected number of interviews.
- **Q5.4 — Sort by vᵢ − cᵢ/pᵢ, highest first.** Swap two adjacent candidates and compare. i goes before j iff
  vᵢ − cᵢ/pᵢ > vⱼ − cⱼ/pⱼ. Skip anyone with pᵢvᵢ < cᵢ, because interviewing them has negative expected value.
- **Q5.5 — Skip the first ≈ n/e, then hire the first best-so-far. P → 1/e ≈ 0.368.**
  - Skip r: P = (r/n) Σ_{k=r+1}^{n} 1/(k−1). For n = 4, skipping 1 gives 11/24 ≈ 0.458, which is optimal.
- **Q5.6 — It isn't worse. The problem gets harder as n grows:** random guessing gives 1/n → 0. Picking the
  single best of a million candidates about 37% of the time is remarkable. The success probability starts at
  1/2 (n = 3) and decreases toward 1/e.
- **Q5.7 — Bayes, then test adaptively.** Start at ⅓ each. After a test, update: posterior(A) =
  (0.8·⅓) / (0.8·⅓ + 0.2·⅔) = **2/3**. Test the current most-likely candidate, or whichever test is most
  informative. Stop when a posterior passes a threshold or the test costs more than the information is worth.
