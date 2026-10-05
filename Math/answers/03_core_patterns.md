# Answers 3: Core patterns (Q14–Q19)

Questions: [../questions/03_core_patterns.md](../questions/03_core_patterns.md)

---

## Q14. Die-roll game: expected value and when to stop

**Answer: $3.50.**

- **Q14.1 — Keep 4 or higher. The game is worth 4.25.** Rerolling is worth 3.5, so keep anything above that.
  ½·5 + ½·3.5 = 4.25.
- **Q14.2 — First roll: keep 5 or higher. The game is worth 14/3 ≈ 4.67.** With two rerolls left, the
  continuation is worth 4.25. (2/6)·5.5 + (4/6)·4.25 = 14/3.
- **Q14.3 — 91/6 ≈ 15.17.** (1 + 4 + 9 + 16 + 25 + 36)/6. Note that this isn't 3.5² = 12.25, because E[X²] ≠ E[X]².
- **Q14.4 — Keep 3 or higher. The game is worth 23/6 ≈ 3.83.** A reroll is worth 3.5 − 1 = 2.5.
  (4/6)·4.5 + (2/6)·2.5.
- **Q14.5 — Quote a bid/ask around 4.25 and explain the width.** For example, 4.00 @ 4.50. It can be tight because
  the EV is known exactly. Widen it if there's risk you can't hedge or if the counterparty might know
  something (a loaded die?). If someone lifts your ask, ask yourself why before you move your quote.

---

## Q15. Expected waiting times for patterns

**Answer: 2 flips, and 6 rolls** (geometric distribution: expected wait = 1/p).

- **Q15.1 — HH: 6. HT: 4.**
- **Q15.2 — Overlap.** A failed HH attempt sends you back to the start. A failed HT attempt doesn't.
  - HH: E₀ = 1 + ½E₁ + ½E₀ and E₁ = 1 + ½·0 + ½E₀, which gives E₀ = 6.
  - HT: E₀ = 1 + ½E₁ + ½E₀ and E₁ = 1 + ½E₁ (once you have an H, a T finishes and another H keeps you in the same state), which gives E₁ = 2 and E₀ = 4.
- **Q15.3 — 14.7.** 6·(1 + ½ + ⅓ + ¼ + ⅕ + ⅙), the coupon collector problem.

---

## Q16. Conditional probability and Bayes

**Answer: 50%.** Out of 10,000 people, 99 are sick and test positive, and 99 are healthy and test positive.

- **Q16.1 — ≈ 99%.** The prior odds are 1:99. Each positive multiplies the odds by 99, so 1:99 → 99:99 → 99²:99 = 99:1.
- **Q16.2 — 1/3.** The equally likely cases are BB, BG, GB.
- **Q16.3 — 1/2.**
- **Q16.4 — Switch. Switching wins 2/3.** The host's choice gives you information because the host *never* opens the car door.
- **Q16.5 — Switching wins 99/100.** That's the intuitive version of the argument.
- **Q16.6 — 1/2. Switching doesn't matter.** A random host who happens to show a goat gives you no information
  beyond ruling out that door.

---

## Q17. Linearity of expectation

**Answer: 1.** Each person gets their own hat with probability 1/n. Add over n people.

- **Q17.1 — → 1/e ≈ 0.368** (derangements).
- **Q17.2 — 48/5 = 9.6.** The 4 aces split the 48 other cards into 5 gaps of equal expected size.
- **Q17.3 — 161/36 ≈ 4.47.** Σₖ P(max ≥ k) = Σₖ [1 − ((k−1)/6)²].

---

## Q18. Gambler's ruin

**Answer: i/N.** Your wealth is a fair martingale, so i = N·P + 0·(1 − P).

- **Q18.1 — i(N − i).**
- **Q18.2 — [1 − (q/p)ⁱ] / [1 − (q/p)ᴺ]**, where q = 1 − p.

---

## Q19. Fermi estimation

**Method:** break the estimate into factors, state each assumption, and give an order of magnitude and a range.

Piano tuners in NYC, as an example:
- About 8.5M people → about 3.5M households. Maybe 1 in 20 has a piano → about 175k, plus schools, churches, and
  venues → **about 200k pianos**.
- Tuned about once a year → about 200k tunings per year.
- One tuner does about 4 a day × 250 days → about 1,000 per year.
- → **about 200 tuners.**

- **Q19.1 — Give an honest range** by pushing the most uncertain factor (pianos per household) up and down. For
  example, a 90% interval of 80–600. Say which assumption drives the width. Don't overclaim.
- **Q19.2 —** Bet at odds that match your interval. At 90% confidence you should be willing to risk up to $9 to win
  $1 that the true value is inside your range. If you wouldn't take that bet, your interval is too narrow.
