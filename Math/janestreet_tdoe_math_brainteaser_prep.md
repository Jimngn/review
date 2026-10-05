# Jane Street TDOE Superday: Math / Probability / Brainteaser Prep

> **To practice, use `questions/` + `answers/` instead (see `00_README.md`).** This file has the questions and
> answers together, so it's for a final skim, not self-testing. The answer keys also include answers to
> follow-ups this file leaves open.

How to use this:
- **List 1 (Essential)**: know every question and follow-up well enough to explain it out loud from scratch.
  Section 1A has the questions you got in round 1. Interviewers often go back to the same themes,
  so the follow-ups matter more than the base answers.
- **List 2 (Extra)**: work through it once List 1 is automatic.
- Answers are short on purpose. In the interview, **say your assumptions out loud, check your
  answer against a sanity bound, and treat each follow-up as the real question.**
- When a question is ambiguous (like your dice question), **ask about the rule before you
  solve**. That counts in your favor.

---

# LIST 1: ESSENTIAL (know 100%)

## 1A. Questions you were asked in round 1 (expect variants or deeper follow-ups)

### Q1. Rollercoaster average speed
1-mile loop. Loop 1 at 70 mph, loop 2 at 50 mph. What's the average speed?
- **Answer:** total distance / total time = 2 / (1/70 + 1/50) = **58.33 mph** (the harmonic mean, not 60).
- **Trap:** 60 is wrong because you spend more *time* at the slower speed.
- Follow-ups:
  - *How fast must loop 2 be to average 60?* 2/(1/70 + 1/v) = 60, so 1/v = 1/30 − 1/70, giving **v = 52.5 mph**.
  - *Loop 1 at 35 mph. Can you average 70?* **No.** That needs 2/70 hr = 1/35 hr total time, and loop 1 already used all of it (loop 2 would need infinite speed).
  - *When is the answer exactly 60?* When you spend equal **time** (not distance) at each speed.
  - *n loops at speeds v₁…vₙ?* The harmonic mean n / Σ(1/vᵢ). It's always ≤ the arithmetic mean.

### Q2. Dice vs. two other players
You and 2 others each roll a die. The highest roll wins. Ties get rerolled. What's P(you win)?
- **First, ask what triggers a reroll:** any tie for the top, or only a tie involving you?
- **Answer:** by symmetry, **1/3** (rerolls don't break the symmetry).
- **Follow-up: the other two both roll a 4. What's your probability?**
  - Rule A (reroll only if you tie the top): win on a 5 or 6 (2/6). Roll a 4 → 3-way tie → reroll → 1/3. Roll 1–3 → lose.
    P = 2/6 + (1/6)(1/3) = **7/18 ≈ 0.389**
  - Rule B (any tie for the top means everyone rerolls): rolling 1–3 leaves the other two tied at the top, so everyone rerolls and you get 1/3 again.
    P = 2/6 + (4/6)(1/3) = **5/9 ≈ 0.556**
  - Point out that the rule changes the answer. That's the insight they're looking for.
- More follow-ups:
  - *One opponent rolled a 4 and the other hasn't rolled yet.* Work through each of your rolls, with a reroll when you tie.
  - *n players?* 1/n by symmetry.
  - *You roll first and see your number. Would you pay $X to play for $Y?* Compute EV based on your roll.
  - *P(no tie among 3 dice)?* (6·5·4)/216 = **5/9**.
  - *Expected max of 3 dice?* Σ P(max ≥ k) = Σₖ [1 − ((k−1)/6)³] ≈ **4.96**.

### Q3. 100th digit of 123456789101112…
- **Answer:** 1–9 use 9 digits. That leaves 91. Two-digit numbers from 10 upward: 45 full numbers (10–54) use 90 digits, so the 99th digit ends "54". The 100th digit is the first digit of 55, which is **5**.
- Follow-ups:
  - *1000th digit?* 9 + 180 = 189 digits through 99. 1000 − 189 = 811 = 270·3 + 1. Numbers 100–369 end at digit 999, so digit 1000 is the first digit of 370: **3**.
  - *How many digits to write 1–100?* 9 + 180 + 3 = **192**.
  - *How many times does "1" appear in 1–100?* 10 in the ones place + 10 in the tens place + 1 in 100 = **21**.
  - *Sum of all digits in 1–100?* In 00–99, each digit appears 20 times: 45·20 = 900. Add 1 for 100: **901**.
  - *How many times do you write "0" in 1–100?* 9 (10,20,…,90) + 2 (100) = **11**.

### Q4. Bus every 20 min: run (5 min) vs. walk (10 min)
- **Expected wait at the stop:** **10 min either way.** With no information, the bus's position in its cycle is uniform when you arrive.
- **Follow-up 1: expected total time until boarding?** Run: 5 + 10 = **15**. Walk: 10 + 10 = **20**.
  - Check: running only matters when the bus arrives 5–10 min from now (probability 5/20 = 1/4). In that case running saves 20 min. 1/4 × 20 = 5. ✓
- **Follow-up 2: known schedule (0, 20, 40, …).** Let τ = minutes until the next bus.
  - τ < 5: you miss it either way, so both board at τ + 20. Indifferent, so walk.
  - 5 ≤ τ < 10: **run.** Running catches it; walking means waiting 20 more minutes.
  - τ ≥ 10: you catch the same bus either way. Indifferent, so walk.
- **Follow-up 3: you only care about time until boarding, not walking vs. waiting.** The answer doesn't change. Running only helps when it gets you onto an *earlier bus*. Otherwise you just trade walking time for waiting time.
- **Follow-up 4: running costs c minutes.**
  - Known schedule: run iff 5 ≤ τ < 10 **and c < 20**.
  - Unknown schedule: the expected saving is 5 min, so run iff **c < 5**.
- More follow-ups:
  - *Buses arrive as a Poisson process averaging every 20 min.* Expected wait = **20** (memoryless). That's the **inspection paradox**: you tend to arrive during longer gaps.
  - *Irregular gaps X.* Expected wait = E[X²] / (2E[X]), which is ≥ E[X]/2.
  - *You see a bus pull away just as you arrive.* Known schedule: wait = 20. Poisson: still 20.

### Q5. Hiring a CEO (secretary problem), 3 candidates
- **Hire the first candidate:** P(best) = **1/3**.
- **Skip the first, then hire the first candidate better than them:** P(best) = **1/2**. This is optimal for n = 3.
  - Check all 6 orderings (1 = best): 123✗ 132✗ 213✓ 231✓ 312✓ 321✗ → 3/6.
  - Outcome distribution: best 1/2, 2nd 1/3, worst 1/6.
- **Follow-up: you only need a competent CEO. Each is independently competent with probability p, and you can observe competence.** Hire the first competent one. P = **1 − (1−p)³**. The order doesn't change the success probability.
- **Follow-up: you can only see relative ability, and competence is a hidden threshold.**
  - The best overall is competent if at least 1 is competent; the 2nd-best if at least 2 are; the worst only if all 3 are.
  - Skip-1 strategy: P(competent) = ½[1−(1−p)³] + ⅓[3p² − 2p³] + ⅙p³.
  - Hire-first strategy: P = p.
  - Skip-1 wins (for example, p = 0.9 gives about 0.945 vs. 0.90). Say why: being best-so-far is correlated with being competent.
- **Follow-up: A = 70%, B = 50%, C = 30% competent. You pick the order.**
  - If you stop at the first competent one, P(success) = 1 − 0.3·0.5·0.7 = **0.895** in *any* order.
  - Order still matters for **cost/time.** Interview the most-likely-competent first (A, B, C) to minimize expected interviews.
- **Follow-up: candidate i has p_i (good), v_i (value if good), and c_i (interview cost).** You hire the first good one.
  - Swap two adjacent candidates and compare. i goes before j iff **v_i − c_i/p_i > v_j − c_j/p_j**. Sort by that index.
  - Skip anyone with p_i·v_i < c_i. Interviewing them has negative expected value.
- **Follow-up: n candidates.** Skip the first ≈ n/e, then hire the first best-so-far. P → **1/e ≈ 0.368**.
  - For n = 4, skipping 1 gives 11/24 ≈ 0.458.
  - General formula: skip r, then P = (r/n) Σ_{k=r+1}^{n} 1/(k−1).
- **"Why is 1/e worse than the 1/2 you got with 3?"** It isn't worse. The problem gets harder as n grows: random guessing gives 1/n → 0. Still picking the single best of a million candidates about 37% of the time is remarkable. The success probability starts at 1/2 (n = 3) and decreases toward 1/e.
- **Follow-up: exactly one of 3 is competent, and you can run noisy tests.** Start with a prior of 1/3 each. Update with Bayes after each test. Test the current most-likely candidate, or whichever test is most informative. Stop when the posterior passes a threshold or the test cost exceeds the value of more information.
  - Example: a test with 80% accuracy flags A as competent. Posterior(A) = (0.8·⅓) / (0.8·⅓ + 0.2·⅔) = **2/3**.

## 1B. Questions reported by other TDO/TDOE candidates

### Q6. Strawberry / water content
- 99% water, 100 g. Dry to 98% water. New weight? The dry part stays at 1 g, which is now 2% of the total, so **50 g**.
- 98% water, 1 g. How much water to drain to reach 50%? Dry part = 0.02 g, which is 50% of the total → total 0.04 g, so drain **0.96 g**.
- Follow-ups: 60% → 50% water? Dry 40% becomes 50%, so the weight scales by 4/5. General formula: new weight = W·(1−a)/(1−b).
  Explain *why* the dry mass stays fixed. They push on this.

### Q7. Minimum bills to pay any amount from $1 to $100
- **Choose any denominations:** powers of 2 (1, 2, 4, 8, 16, 32 cover up to 63) plus one bill between 37 and 64 → **7 bills**. 6 bills give only 2⁶ − 1 = 63 nonzero sums, so 7 is the minimum.
- **US bills only:** ones digit 0–9 needs {1, 2, 2, 5} (3 bills give only 7 subsets). Tens digit 10–100 needs {10, 20, 20, 50} → **8 bills**.
- Follow-ups: make up to $N? About ⌈log₂(N+1)⌉ bills. What if you're making change instead of paying (using bills you receive)? Different problem, so clarify first.

### Q8. Coins and counting
- 5 flips, exactly 3 heads: C(5,3)/32 = **5/16**.
- At least 3 heads in 5: (10 + 5 + 1)/32 = **1/2** (by symmetry).
- P(even number of heads) in 6 flips: **1/2**. In 99 fair coins plus 1 biased coin: still **1/2**, because a single fair coin makes the parity 50/50.
- 5-letter palindromes: the first 3 letters decide the rest, so 26³ = **17,576**.
  - Follow-up: 6 letters → 26³. With no repeated letters → 26·25·24 (5-letter).

### Q9. Largest 3-digit number that's a sum of 2, 3, AND 5 consecutive integers
- Sum of 2 consecutive → odd. Sum of 3 → multiple of 3. Sum of 5 → multiple of 5. So you need an odd multiple of 15.
- 990 is even, so the answer is **975**.
- Follow-up: 2, 3, 4, and 5? A sum of 4 consecutive = 4k + 6, which is ≡ 2 (mod 4) and even. That conflicts with "odd", so it's **impossible**.

### Q10. Digit products
- Smallest number whose digits multiply to 96: no 2-digit number works (max product 81). The 3-digit options are {2,6,8}, {3,4,8}, {4,4,6}, so the answer is **268**.
- "Largest": **unbounded** if 1s are allowed. Point that out. Without 1s, use the most digits possible: 2·2·2·2·2·3 → **322222**.

### Q11. Two people meeting
Each arrives at a uniform random time within an hour and waits 20 min. P(they meet)? 1 − (40/60)² = **5/9**.
- Follow-ups: waiting w out of T gives 1 − (1 − w/T)². Different waiting times: draw it geometrically as a square minus two triangles.

### Q12. Train vs. walking (reported in London TDO interviews)
Same structure as Q4 with the train every 10 min, a 5-min ride, and a 10-min walk.
- Train: E[wait] = 5, plus a 5-min ride, so 10 min expected vs. 10 min walking. **Tie in expectation.** Walking has zero variance, which matters if you're late.
- Expect them to keep adding factors: walk to the station, uncertainty in the train timetable, and variance vs. mean.

### Q13. Other reported quick ones
- Rain on at least one weekend day, each day 50%, independent: 1 − 0.25 = **75%**. Follow-up: correlated days → inclusion-exclusion needs P(both).
- Two cards, both kings: (4/52)(3/51) = **1/221**.
- Clock angle at 9:30: hour hand at 285°, minute hand at 180°, so **105°**. General formula: |30H − 5.5M|.
- Day of the week 10 years from today: 3650 ≡ 3 (mod 7), plus 2–3 leap days, so **+5 or +6 days**.

## 1C. Core patterns every Jane Street superday tests

### Q14. Die-roll game with rerolls (EV and optimal stopping)
Get paid the face value of a die.
- Fair price: **3.5**.
- One reroll allowed: keep 4 or higher, giving ½·5 + ½·3.5 = **4.25**.
- Two rerolls: keep 5 or higher, giving (2/6)·5.5 + (4/6)·4.25 = **14/3 ≈ 4.67**.
- Follow-ups: paid the square of the roll (91/6 ≈ 15.17)? Each reroll costs $1? **"Make me a market."** Give a bid/ask around your EV and explain the width.

### Q15. Expected waiting times for patterns
- Flips until the first head: **2**. Rolls until a 6: **6** (geometric distribution).
- Flips until HH: **6**. Until HT: **4**.
  - Follow-up: explain why they differ (overlap / self-similarity). Set up the state equations.
- Collect all 6 die faces: 6·(1 + ½ + … + ⅙) = **14.7** (coupon collector).

### Q16. Conditional probability and Bayes
- Disease with 1% prevalence, 99% sensitivity, 1% false-positive rate. You test positive: **50%**.
  - Follow-up: test twice, both positive → about 99%.
- Two children, at least one is a boy. P(both boys) = **1/3**.
  - "The older one is a boy" → **1/2**.
- Monty Hall: switching wins **2/3**. Follow-ups: 100 doors? A host who opens a door at random (and happens to show a goat) → 1/2.

### Q17. Linearity of expectation
- Hats shuffled: expected number of correct matches = **1**. P(no matches) → 1/e.
- Expected number of cards before the first ace: 48/5 = **9.6**.
- Expected max of 2 dice: 161/36 ≈ **4.47**.

### Q18. Gambler's ruin / random walk
- Fair ±$1 bets, start at $i. P(reach $N before $0) = **i/N**.
- Follow-ups: expected duration = i(N − i). Biased coin: ((q/p)^i − 1)/((q/p)^N − 1).

### Q19. Fermi estimation
Examples: piano tuners in NYC, trades on the NYSE per day, golf balls in a plane.
- Break it into factors. State each assumption. Give an order of magnitude and a range.
- Follow-up: **"How confident are you? Give a 90% interval. Would you bet on it?"**

## 1D. Practice set: categories and follow-ups (added from your notes, with answers checked)
Format to expect: about 3 questions, roughly 10 min each, with 1–3 follow-ups per question.
⚠️ = the original notes had an error or an unsolvable setup. It's corrected here, and each
one is a good "ask a clarifying question" moment.

### Q20. Die: keep or reroll once (extends Q14)
- Keep 4–6, reroll 1–3. EV = **4.25**. Two rerolls → **14/3**.
- *20-sided die:* keep if the roll beats (n+1)/2 = 10.5, so keep 11–20. EV = ½·15.5 + ½·10.5 = **13**.
- *Each reroll costs $1:* a reroll is worth 3.5 − 1 = 2.5, so keep 3 or higher. EV = (4/6)·4.5 + (2/6)·2.5 = **23/6 ≈ 3.83**.
- *Fixing a threshold before seeing the roll:* same answer, because a threshold strategy is already optimal. Say why: the decision depends only on the current roll compared with the value of continuing.

### Q21. 3 coins, exactly 2 heads
- **3/8**. At least 2 → **1/2**. Biased coin: **3p²(1−p)**.
- Expected flips until HH → **6**. Expected flips until the first head → **1/p**.

### Q22. Meeting at a coffee shop (extends Q11)
- 1 hour, each waits 20 min → **5/9**.
- *A waits 10, B waits 20:* they miss if B arrives more than 10 min after A (triangle with legs 50) or A arrives more than 20 min after B (legs 40).
  P(meet) = 1 − (1250 + 800)/3600 = **31/72 ≈ 0.43**.
- ⚠️ *2-hour window, still waiting 20 min:* the answer **does change**. Only the ratio w/T matters, and it drops to 1/6: 1 − (5/6)² = **11/36 ≈ 0.31**.
  The answer only stays 5/9 if the wait also doubles. (The original notes got this wrong.)
- *Three people, each waits 20 min, all present at once:* you need (last arrival − first arrival) ≤ 20, so d = 1/3.
  P = 3d² − 2d³ = **7/27 ≈ 0.26**.
- *Simulation:* draw random pairs of arrival times, count the fraction with |x − y| ≤ 20, and use the √N error bar to justify the sample size.

### Q23. Bus: work backward
Half get off and 3 get on. Then a third get off and 5 get on. Now there are 20. How many started?
- ⚠️ Working backward: 20 − 5 = 15 = (2/3)·x, so x = **22.5**. That's not a whole number, so **the puzzle as stated is impossible.**
  Saying this out loud is exactly the "integer constraint" twist they're testing.
- Fixed version (ending with 21): 21 → 24 before stop 2 → 42 at the start. Check: 42 → 21 + 3 = 24 → 24 − 8 + 5 = 21 ✓.
- *Integer constraints:* the starting number must be even, and (start/2 + 3) must be divisible by 3. Together: start ≡ 0 (mod 6).
- *General pattern:* write each stop as xₖ₊₁ = aₖ·xₖ + bₖ and invert step by step.

### Q24. Next date (DD/MM/YYYY) with all 8 digits different
- **17/06/2345.**
- Reasoning: the day must start with 0–3 and the month with 0 or 1, so the day and month together must use **both 0 and 1**.
  Then the year can't use 0 or 1, so the smallest year is 2345. Months and days come from {6, 7, 8, 9}: month 06, day 17.
  (Years 20xx, 21xx, and 22xx all fail. Show why.)
- *YYYY-MM-DD format:* same digits, so the **same answer.** It shows you understand the method.
- *Day of the week in 10 years:* +5 or +6 days (see Q13).
- *P(a random date has all distinct digits):* count valid (day, month) pairs with distinct digits, then count years that avoid those digits. Set up the counting; you don't need to finish it.

### Q25. Two children (extends Q16)
- At least one boy → **1/3**. Older child is a boy → **1/2**.
- At least one boy born on a Tuesday → **13/27**. (27 = 14² − 13² combinations include a Tuesday boy; 13 of them are two boys.)
- 3 children, at least one boy: P(all boys) = **1/7**.

### Q26. Matching coins with a partner
- ⚠️ As written, there's **no decision to make**: P(match) = p² + (1−p)², which is ≥ ½.
  Ask **what you actually control.** If you can choose which side to show, agree beforehand on "both show heads" → **100%**.
- Unknown bias: by symmetry you can't do better than a pre-agreed rule.
- 100 games: the number of matches ~ Binomial(100, p² + (1−p)²). Strategy still affects each game's probability, and the law of large numbers makes the total predictable.

### Q27. Strawberry and mixtures (extends Q6)
- 98% water, 100 g, dries to 50% water → dry 2 g → **4 g**.
- Dries to 90% water → 2/0.10 = **20 g**.
- *Adding dry mass* to go from 98% to 90% water: water stays at 98 g, which is 90% of the new total → total 108.9 g, so add **≈ 8.9 g**.

### General follow-up patterns (across all categories)
- "Change one parameter" means they're testing whether you understand the method, not whether you memorized the answer.
- "Check that a different way": use a limiting case, symmetry, simulation logic, or a bounds check.
- "How confident are you?" Give an honest range. Don't overclaim.
- If they just move on with no follow-up, that usually means you answered cleanly. Don't panic.

---

# LIST 2: EXTRA (if time allows)

### Geometric probability
- Break a stick at 2 random points. P(the 3 pieces form a triangle) = **1/4**. Follow-up: break once, then break the longer piece.
- 3 random points on a circle all in one semicircle: **3/4**. With n points: n/2^(n−1).
- Random chord longer than the triangle side: **ill-posed (Bertrand's paradox).** Ask how the chord is chosen.

### Dice and cards
- P(at least one 6 in 4 rolls) = 1 − (5/6)⁴ ≈ **0.518**, vs. at least one double-six in 24 rolls of 2 dice ≈ **0.491** (de Méré).
- P(sum of 2 dice = 7) = **1/6**. Most likely sum of 3 dice: **10 or 11**.
- Deck of cards, draw until the first red card. Expected draws: 53/27 ≈ **1.96**.
- Draw cards one at a time and say "stop" whenever you like, betting that the next card is red. Best strategy? **Every strategy gives 1/2** (martingale).

### Expected value / betting
- St. Petersburg game: infinite EV. Why wouldn't anyone pay much? Utility, and a finite bankroll for the counterparty.
- Kelly bet with edge p on even odds: bet fraction **2p − 1**.
- "I'll give you the higher of two dice rolls. What's the price?" → 161/36. Then *"make me a market,"* and *"I'm buying at your ask. Update?"*

### Logic puzzles
- 25 horses, 5 per race, find the top 3: **7 races**.
- 2 eggs, 100 floors: **14 drops** (14 + 13 + … ≥ 100).
- 12 coins, one counterfeit (heavier or lighter), balance scale: **3 weighings**.
- Bridge and torch (1, 2, 5, 10 minutes): **17 minutes**.
- Two ropes that each burn in 60 min (unevenly). Measure 45 min: light rope 1 at both ends and rope 2 at one end. When rope 1 burns out (30 min), light the other end of rope 2 → 15 more minutes.
- 100 lockers toggled by each divisor: the open ones are perfect squares, so **10**.
- Ants on a 1 m stick: bouncing is equivalent to passing through, so the max time = time to walk the full length.
- Pirate gold splitting: backward induction.

### Number sense (quick checks)
- Trailing zeros of 100!: 20 + 4 = **24**.
- Last digit of 7¹⁰⁰: cycle 7, 9, 3, 1 → **1**.
- Sum 1…100 = **5050**. Sum of squares 1…n = n(n+1)(2n+1)/6.
- Handshakes among n people = n(n−1)/2.
- Mental math drills: 17 × 32, 1/7 as a decimal, 15% of 840, √200. Practice being fast *and* checking your own answers.

### Game theory
- You and I pick numbers 1–100. Closest to 2/3 of the average wins. Iterated reasoning.
- Russian roulette with 2 adjacent bullets in a 6-chamber revolver, one pull already survived: **don't spin** (P(survive) = 3/4 vs. 2/3 if you spin).
- Two players take turns flipping a coin, first head wins. P(the first player wins) = **2/3**.

---

## Interview technique checklist (from reported feedback)
- Think out loud and don't go silent. Interviewers give hints when you're stuck, but only if they can follow your reasoning.
- Check your answers ("58 is between 50 and 70 and closer to 50, which makes sense because I spend longer at 50").
- Ask about ambiguous rules before solving (dice tie rule, "largest" with 1s allowed).
- For each follow-up, first say **what changed and why it matters**, then compute.
- Be friendly. One candidate's GDPR request showed they were rejected mainly for not seeming friendly enough.
