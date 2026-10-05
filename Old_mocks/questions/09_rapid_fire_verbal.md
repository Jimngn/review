# Mock 9 — Rapid-Fire Verbal Bank (no coding, ~30 min)

These are the questions that get fired at you *between* coding tasks, usually while your
code is still on screen. They're scored on whether the answer is immediate and confident —
a correct answer delivered after fifteen seconds of silence reads as a guess.

**How to drill this:** answer out loud, in under 20 seconds each, *before* reading the key.
Record yourself if you can. Repeat the set until all of them are reflexive.

---

## Set A — complexity of your own code
1. What's the complexity of `sorted(x)`? Of `max(x)`? Of `x in some_list` vs `x in some_set`?
2. What's the complexity of `list.pop(0)` vs `list.pop()`? Why the difference?
3. What's the complexity of `dict[key]` lookup — and when is it *not* that?
4. You wrote a loop inside a loop. Is it always O(n^2)?
5. Your matching loop is `while` inside `while`. Why isn't that quadratic in book size?
6. What's the space complexity of your solution? Does the output count?
7. "Make it faster" — what's the first question you ask back?

## Set B — data structure choice
8. Why a `deque` and not a `list` for a price level?
9. Why a `dict` of prices and not a sorted list of all orders?
10. When would you use a heap instead of sorting?
11. Why can't you use a heap to print the whole book in price order cheaply?
12. What does a `set` give you that a `list` doesn't, and what does it cost?
13. When is a plain list genuinely the right answer over anything fancier?
14. What's the data structure for O(1) cancel by order ID?

## Set C — edge cases, asked cold
15. What does your function do on an empty input?
16. What does it do on an input of size 1?
17. What if the input has duplicates?
18. What if the input is already sorted? Already reverse sorted?
19. What if there are ties for the top k?
20. What if quantities are zero? Negative?
21. What if two things arrive at the exact same timestamp?
22. Where could this loop fail to terminate?

## Set D — the trading-context questions
23. Why do exchanges use price-time priority rather than, say, pro-rata?
24. Why does the trade happen at the resting order's price and not the incoming one's?
25. What is the spread, and what does a wide spread tell you?
26. Why is trading with yourself a problem?
27. Why would someone send an order that cancels whatever doesn't fill immediately?
28. What's the difference between realized and unrealized P&L?
29. Why would you store prices as integers?

## Set E — the questions they ask you at the end
30. "What questions do you have for me?" — have **three** ready, and none of them should be
    answerable from the careers page. (See the key for what works for a TDOE role
    specifically.)
