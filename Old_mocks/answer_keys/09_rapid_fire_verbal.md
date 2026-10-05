# Answer Key — Mock 9 (Rapid-Fire Verbal)

Target: each answer in one or two sentences, inside 20 seconds.

## Set A — complexity
1. `sorted(x)` is **O(n log n)**. `max(x)` is **O(n)**, one pass. `x in list` is **O(n)**;
   `x in set` or `in dict` is **O(1) average** — that swap is the single most common real
   speedup, turning an O(n^2) loop into O(n).
2. `pop(0)` is **O(n)** — every later element shifts down one slot. `pop()` from the end is
   **O(1)**. This is exactly why a price level uses a `deque`, where both ends are O(1).
3. **O(1) average.** Not that when keys collide heavily (O(n) worst case), or when hashing
   the key itself is expensive — hashing a long string is O(length). Unhashable keys (a
   list) don't work at all.
4. **No.** It's O(n x m) where m is the *inner* loop's actual trip count. If the inner loop
   runs a bounded number of times, or the two loops together touch each element once (as in
   a merge or a two-pointer scan), it's O(n).
5. Because the inner loop is bounded by **orders consumed, not orders resting**. Every
   resting order can be consumed at most once in its lifetime, so the cost is *amortized*
   across all the orders that ever rested — a single sweep can be expensive, but the
   average per order stays small.
6. State **extra** space, excluding the input. Returning a list of k items is O(k) output;
   the top-3 tracker is O(1) extra. Say which you're counting — that precision reads well.
7. **"Faster for what input?"** Small k and huge n points to a heap; many repeated queries
   points to precomputation or an index; a big constant factor points to profiling, not big-O.
   The question also establishes whether they mean asymptotics or wall-clock.

## Set B — data structures
8. A price level needs **FIFO**: append at the back, pop from the front. `deque` is O(1)
   both ends; `list.pop(0)` is O(n), so a busy level would degrade quadratically.
9. Because you need two different accesses: **find a price instantly** (dict, O(1)) and
   **preserve arrival order within that price** (deque). A single sorted list of all orders
   makes insertion O(n) and gives you nothing extra.
10. When you need the **top k, not the full order** — O(n log k) beats O(n log n), and the
    gap matters when k << n. Also for a running/streaming top-k, where you can't re-sort.
11. A heap only guarantees the **root** is the minimum; the rest is partially ordered. Getting
    everything in order means draining it — O(P log P), no better than sorting. That's why a
    full book display wants a sorted container or a tree, not a heap.
12. A set gives **O(1) membership and automatic dedupe**; it costs you **ordering and
    duplicates**, plus the elements must be hashable, plus extra memory for the hash table.
13. When n is small, when you need indexing or ordering, or when you'll iterate the whole
    thing anyway. **A list scan of 10 items beats a dict with a clever key every time** —
    and saying this shows judgment rather than reflex.
14. A **hash map from order ID to the order**, plus either a **doubly-linked list** per price
    level (unlink in O(1) with no search) or **lazy deletion** (flag it inactive, skip it
    when matching). Real exchanges use the linked list.

## Set C — edge cases
15. Decide and say it: return `None`, return empty, or raise. The wrong answer is "I hadn't
    thought about it." For a max, `None` or an exception; for a filter, empty is natural.
16. Usually fine, but it's where off-by-one and "compare to the next element" logic breaks.
17. Ask whether duplicates are **distinct events** (two real trades) or **errors**. Top-3 of
    `[90, 90, 40]` is `[90, 90, 40]` unless they asked for distinct values — confirm which.
18. Already-sorted is the best case for insertion-sort-like approaches and the **worst case
    for naive quicksort pivoting**. Reverse-sorted maximizes swaps in many algorithms. Python's
    `sorted` (Timsort) is O(n) on already-sorted input — a nice fact to have.
19. Ask what they want: all tied items (output longer than k), or an arbitrary/stable k?
    Stable sorting means ties come out in input order, which is often the sane default.
20. Zero quantity: reject — it's meaningless and can cause non-termination in a matching
    loop. Negative: reject at the boundary so the core logic can trust its input.
21. A **monotonic sequence number assigned on receipt**. Timestamps have finite resolution
    and can tie; the sequence is what actually defines priority.
22. Anywhere a loop's progress depends on a quantity decreasing — if it can be zero, the
    loop spins. Also `while` loops over a structure you mutate inside the loop. Flagging this
    unprompted is a strong signal.

## Set D — trading context
23. **Price-time rewards both aggression and being early**, which incentivizes posting tight
    quotes quickly — that's how an exchange gets liquidity. It's also simple, deterministic,
    and auditable: anyone can verify who should have filled. (Pro-rata exists too, mostly in
    some futures markets, and favors size over speed.)
24. The resting order **set the terms and was there first** — the incoming trader chose to
    accept them. It also means posting a limit order can never fill you at a worse price than
    you asked for, which is the guarantee that makes resting safe. Stated in Jane Street's own
    primer: the trade occurs "at the price of the order that was already listed."
25. **Spread = best ask - best bid**, the round-trip cost of trading immediately. A wide
    spread means low liquidity, high uncertainty, or high risk to the market maker — it's
    compensation for the risk of being picked off.
26. It creates a **printed trade at a price you chose with no change in your position** —
    fake volume that can mislead other participants about activity and price. That's wash
    trading, and it's a regulatory issue, which is why exchanges build in prevention.
27. Because **resting on the book leaks information and creates risk**. If you only want a
    fill at the current price and don't want to advertise your interest or be left exposed
    if the market moves, IOC gets you the fill-or-nothing without posting.
28. **Realized** is locked in by closing a position — it doesn't change. **Unrealized** is
    the mark-to-market value of what you still hold, and it moves every time the price moves
    without you doing anything. Nice extra: the cost convention (FIFO/LIFO/average) shifts
    P&L between the two buckets but never changes the total.
29. **Floats don't compare exactly** — `0.1 + 0.2 != 0.3`. An exchange's core operation is
    comparing prices for equality and ordering, so a float rounding error means orders
    silently fail to cross. Store cents (or ticks) as integers.

## Set E — your questions for them
Three that work for a **trading desk operations / TDOE** role specifically, because they're
about the actual job and can't be answered from the website:

- *"When something breaks mid-session — a feed goes down, or a position looks wrong — what
  does the first ten minutes actually look like, and who's in the room?"* Shows you're
  thinking about the operational reality rather than an idealized job description.
- *"How much of the role is responding to things versus building tooling to stop them
  recurring, and how has that mix changed as the desk has grown?"* Signals you want to build,
  which is the growth path in this role.
- *"What separates someone who's good at this after a year from someone who's exceptional?"*
  Invites a candid answer and tells you exactly what's valued.

Avoid: anything about comp, WLB, or "what's the culture like" in this round — all fine
later, but here they spend a question on something you could have looked up.

**Also be ready for the mirror**: *"Why trading? Why Jane Street? Why this role rather than
a software engineering role?"* Have a 60-second answer. For TDOE, the honest and strong
version is usually some combination of: you want the feedback loop of a live system where
mistakes are visible immediately, you like the mix of ops judgment and building tools, and
you want to be close to the actual trading rather than two abstraction layers away.
