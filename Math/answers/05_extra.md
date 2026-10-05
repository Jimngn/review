# Answers 5: Extra (E1–E25)

Questions: [../questions/05_extra.md](../questions/05_extra.md)

---

## Geometric probability

- **E1 — 1/4.** Every piece must be shorter than ½. Draw it in the unit square: the region where no piece is ½ or
  longer has area 1/4.
  - **E1.1 — 2 ln 2 − 1 ≈ 0.386.** This is higher than 1/4, because breaking the longer piece avoids the worst cases.
- **E2 — 3/4.**
  - **E2.1 — n / 2ⁿ⁻¹.** For each point, the chance that all the others lie in the semicircle clockwise from it is
    (½)ⁿ⁻¹. Those n events can't overlap.
- **E3 — Ill-posed (Bertrand's paradox). Ask how the chord is chosen.** Random endpoints give 1/3, a random point
  along a radius gives 1/2, and a random midpoint gives 1/4.

## Dice and cards

- **E4 — At least one 6 in 4 rolls: 1 − (5/6)⁴ ≈ 0.518.** At least one double-six in 24 rolls: 1 − (35/36)²⁴ ≈ 0.491.
- **E5 — 1/6. The most likely sum of three dice is 10 or 11** (27/216 each).
- **E6 — 53/27 ≈ 1.96.** 1 + (expected number of black cards before the first red) = 1 + 26/27.
- **E7 — Every strategy gives 1/2** (martingale). The fraction of red cards left is a fair game, so you can't time it.

## Expected value and betting

- **E8 — The expected value is infinite:** Σ (½)ᵏ·2ᵏ = Σ 1. Yet nobody pays much, because utility is concave and
  the counterparty's bankroll is finite. For example, if the bank can pay at most 2³⁰, the EV is only about 31.
- **E9 — Bet 2p − 1 (the Kelly criterion).** This maximizes the long-run growth rate of log wealth.
- **E10 — 161/36 ≈ 4.47.**
  - **E10.1 —** Quote around the EV, for example 4.25 @ 4.75. Explain the width: it's a known-EV game, so you can
    be tight. Widen it for risk or if you're unsure about the rules.
  - **E10.2 —** If the dice really are fair and random, your EV doesn't change. **But a trade at your ask is
    information:** does the counterparty know something (a loaded die, different rules)? Move your quote up and/or
    widen it, and say why.

## Logic puzzles

- **E11 — 7 races.** 5 heats, then a race of the 5 winners. The last race is A2, A3, B1, B2, C1 (A is the fastest
  heat winner, B second, C third).
- **E12 — 14 drops.** Drop from 14, then 27 (13 more), then 39, and so on. You need n(n+1)/2 ≥ 100.
- **E13 — 3 weighings.** Start with 4 vs. 4. There are 24 possible answers (12 coins × heavy or light), and 3³ = 27 ≥ 24.
- **E14 — 17 minutes.** 1 and 2 cross (2), 1 returns (1), 5 and 10 cross (10), 2 returns (2), 1 and 2 cross (2).
- **E15 —** Light rope 1 at both ends and rope 2 at one end. When rope 1 burns out (30 min), light the other end of
  rope 2. It burns out 15 minutes later.
- **E16 — 10.** A locker ends open iff it has an odd number of divisors, which happens iff its number is a perfect square.
- **E17 — 1 minute.** When two ants bounce, it looks exactly like they passed through each other. So the maximum is
  the time to walk the full length.
- **E18 — 98, 0, 1, 0, 1** (from most to least senior). Work backward from 2 pirates: D takes 100–0. With 3: C 99,
  D 0, E 1. With 4: B 99, C 0, D 1, E 0. With 5: A buys the 2 votes that are cheapest, C and E.
  Assumes that ties pass and that a pirate who's indifferent votes no.

## Number sense

- **E19 — 24.** ⌊100/5⌋ + ⌊100/25⌋ = 20 + 4.
- **E20 — 1.** The last digits cycle 7, 9, 3, 1, and 100 ≡ 0 (mod 4).
- **E21 — 5050. n(n+1)(2n+1)/6. n(n−1)/2.**
- **E22 — 544. 0.142857 (repeating). 126. ≈ 14.14.** Practice being fast *and* checking yourself.

## Game theory

- **E23 —** In the Nash equilibrium everyone picks 1, by repeatedly eliminating dominated choices. In practice,
  estimate how many rounds of that reasoning other people do. If the room averages about 33, pick about 22. Say
  both answers.
- **E24 — Don't spin.** Without a spin, you survive with probability 3/4: of the 4 empty chambers, only one is
  followed by a bullet. With a spin, it's 4/6 = 2/3.
- **E25 — 2/3.** P = ½ + ¼·P, because the first player wins now or both miss and the game restarts.
