# Questions 3: Core patterns every Jane Street superday tests (Q14–Q19)

Answers: [../answers/03_core_patterns.md](../answers/03_core_patterns.md). Don't open it until the mock is over.

> **Open this in Markdown preview (Cmd+Shift+V)** so the follow-ups stay collapsed. Say your answer
> out loud before opening the next follow-up.

---

## Q14. Die-roll game: expected value and when to stop · ⏱ 10 min

> "I roll a fair die and pay you the face value in dollars. What's a fair price to play?"

<details>
<summary>Follow-up Q14.1</summary>

> "Now you can reroll once, but if you reroll you have to take the second roll. What's your strategy,
> and what's the fair price?"

</details>

<details>
<summary>Follow-up Q14.2</summary>

> "Two rerolls allowed?"

</details>

<details>
<summary>Follow-up Q14.3</summary>

> "No rerolls, but I pay you the square of the roll. Fair price?"

</details>

<details>
<summary>Follow-up Q14.4</summary>

> "One reroll allowed, but the reroll costs you $1."

</details>

<details>
<summary>Follow-up Q14.5</summary>

> "Make me a market on the one-reroll game."

</details>

---

## Q15. Expected waiting times for patterns · ⏱ 10 min

> "On average, how many flips of a fair coin until the first head? How many rolls of a die until the
> first 6?"

<details>
<summary>Follow-up Q15.1</summary>

> "Expected flips until you see HH? Until you see HT?"

</details>

<details>
<summary>Follow-up Q15.2</summary>

> "Why are those two different? Set up the equations."

</details>

<details>
<summary>Follow-up Q15.3</summary>

> "Expected number of die rolls to see all six faces?"

</details>

---

## Q16. Conditional probability and Bayes · ⏱ 10 min

> "A disease affects 1% of people. The test catches 99% of cases and has a 1% false-positive rate.
> You test positive. What's the probability you have it?"

<details>
<summary>Follow-up Q16.1</summary>

> "You take the test again, independently, and it's positive again. Now what?"

</details>

<details>
<summary>Follow-up Q16.2</summary>

> "Different setup: a family has two children, and at least one is a boy. What's the probability both
> are boys?"

</details>

<details>
<summary>Follow-up Q16.3</summary>

> "Instead, you know the older one is a boy. What's the probability both are boys?"

</details>

<details>
<summary>Follow-up Q16.4</summary>

> "Monty Hall: 3 doors, one car. You pick a door, and the host, who knows where the car is, opens
> another door to show a goat. Should you switch?"

</details>

<details>
<summary>Follow-up Q16.5</summary>

> "Same game with 100 doors. The host opens 98 goat doors."

</details>

<details>
<summary>Follow-up Q16.6</summary>

> "Back to 3 doors, but the host opens one of the other doors *at random*, and it happens to show a
> goat. Should you switch?"

</details>

---

## Q17. Linearity of expectation · ⏱ 8 min

> "n people throw their hats in a pile and each takes one at random. What's the expected number of
> people who get their own hat back?"

<details>
<summary>Follow-up Q17.1</summary>

> "What's the probability that nobody gets their own hat, as n gets large?"

</details>

<details>
<summary>Follow-up Q17.2</summary>

> "Shuffle a standard deck. What's the expected number of cards before the first ace?"

</details>

<details>
<summary>Follow-up Q17.3</summary>

> "What's the expected maximum of two dice?"

</details>

---

## Q18. Gambler's ruin · ⏱ 8 min

> "You start with $i and bet $1 on each flip of a fair coin, until you reach $N or go broke. What's the
> probability that you reach $N?"

<details>
<summary>Follow-up Q18.1</summary>

> "What's the expected number of bets before the game ends?"

</details>

<details>
<summary>Follow-up Q18.2</summary>

> "Now the coin is biased: you win each bet with probability p ≠ ½."

</details>

---

## Q19. Fermi estimation · ⏱ 8 min

> "How many piano tuners work in New York City?"
>
> (Other versions to practice: trades on the NYSE per day, golf balls that fit in a plane.)

<details>
<summary>Follow-up Q19.1</summary>

> "How confident are you? Give me a 90% interval."

</details>

<details>
<summary>Follow-up Q19.2</summary>

> "Would you bet on it? At what odds?"

</details>
