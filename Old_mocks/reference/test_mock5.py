"""
Verifies order_book_mock5.py against ALL FOUR worked examples in Jane Street's
"Order Book Basics Primer", plus Mock 5's own parts (partial fills, cancel).

Nothing from Mock 6 is tested here — see test_mock6.py.

Run:  python3 test_mock5.py
"""
from order_book_mock5 import OrderBook, BUY, SELL, to_cents


def check(label, got, want):
    status = "ok  " if got == want else "FAIL"
    print(f"[{status}] {label}\n        got  {got}\n        want {want}")
    assert got == want, label


print("=== Primer 1: Basics — no cross, then a cross at the RESTING price ===")
b = OrderBook()
b.add_order("me", BUY, 15.00, 100)
b.add_order("anne", SELL, 16.00, 100)
check("no trade when bid 15 / ask 16", b.trades, [])
made = b.add_order("bob", SELL, 15.00, 100)
check("bob's offer trades 100 @ $15.00", [(t.qty, t.price) for t in made], [(100, 1500)])
check("book after: only anne's 16.00 offer", b.snapshot(), ([], [(16.00, 100)]))

print("\n=== Primer 2: Price Priority — better-priced offer wins ===")
b = OrderBook()
b.add_order("a1", SELL, 16.00, 100)
b.add_order("a2", SELL, 17.00, 100)
b.add_order("b1", BUY, 15.00, 100)
made = b.add_order("anne", BUY, 17.00, 100)
check("executes against the 16.00 offer, AT 16.00",
      [(t.qty, t.price) for t in made], [(100, 1600)])

print("\n=== Primer 3: Multiple + Partial Executions (Mock 5 Part 4) ===")
b = OrderBook()
b.add_order("bid15", BUY, 15.00, 100)
b.add_order("bid14", BUY, 14.00, 50)
b.add_order("ask16", SELL, 16.00, 100)
b.add_order("ask17", SELL, 17.00, 50)
made = b.add_order("bob", SELL, 14.00, 200)
check("sweeps 100@15.00 then 50@14.00",
      [(t.qty, t.price) for t in made], [(100, 1500), (50, 1400)])
check("leftover 50 rests as an OFFER at 14.00",
      b.snapshot(), ([], [(14.00, 50), (16.00, 100), (17.00, 50)]))

print("\n=== Primer 4: Time Priority — same price, oldest resting order fills ===")
b = OrderBook()
b.add_order("anne", SELL, 16.00, 150)      # first
b.add_order("bob",  SELL, 16.00, 200)      # second
made = b.add_order("you", BUY, 16.00, 100)
check("fills against anne (oldest), not bob",
      [(t.qty, t.price, t.sell_id) for t in made], [(100, 1600, "anne")])
check("anne has 50 left + bob's 200 = 250 at the 16.00 level",
      b.snapshot()[1], [(16.00, 250)])

print("\n=== Mock 5 Part 2: best bid / best ask / snapshot ===")
b = OrderBook()
b.add_order("x1", BUY, 15.00, 100)
b.add_order("x2", BUY, 15.00, 50)
b.add_order("x3", BUY, 14.00, 50)
b.add_order("y1", SELL, 16.00, 100)
check("best bid", b.best_bid(), to_cents(15.00))
check("best ask", b.best_ask(), to_cents(16.00))
check("snapshot aggregates the two orders at 15.00 into one level",
      b.snapshot(), ([(15.00, 150), (14.00, 50)], [(16.00, 100)]))
check("empty side -> None", OrderBook().best_bid(), None)

print("\n=== Mock 5 Part 5: cancel ===")
b = OrderBook()
b.add_order("keep", SELL, 16.00, 100)
b.add_order("gone", SELL, 16.00, 100)
check("cancel returns True", b.cancel("gone"), True)
check("level total drops to 100", b.snapshot()[1], [(16.00, 100)])
check("cancel twice is a harmless no-op", b.cancel("gone"), False)
check("cancel unknown id is a harmless no-op", b.cancel("nope"), False)
made = b.add_order("buyer", BUY, 16.00, 100)
check("cancelled order is skipped; fills against 'keep'",
      [(t.qty, t.sell_id) for t in made], [(100, "keep")])
check("book now empty", b.snapshot(), ([], []))
check("cancel an already-filled order is a no-op", b.cancel("keep"), False)

print("\n=== Mock 5: a cancel that empties a level must remove the level ===")
b = OrderBook()
b.add_order("only", BUY, 15.00, 100)
b.cancel("only")
check("best_bid must NOT report a level of dead orders", b.best_bid(), None)

print("\n=== Mock 5 Part 1: integer cents (the float trap) ===")
b = OrderBook()
b.add_order("f", BUY, 0.10, 100)
b.add_order("g", BUY, 0.20, 100)
check("prices stored exactly, so 0.1/0.2 never drift",
      sorted(b.level_qty[BUY]), [10, 20])

print("\n=== Mock 5: input validation ===")
b = OrderBook()
for label, fn in [
    ("zero quantity rejected",     lambda: b.add_order("z", BUY, 15.00, 0)),
    ("negative quantity rejected", lambda: b.add_order("n", BUY, 15.00, -5)),
    ("negative price rejected",    lambda: b.add_order("p", BUY, -1.00, 10)),
]:
    try:
        fn()
        print(f"[FAIL] {label} — no error raised"); raise SystemExit(1)
    except ValueError as e:
        print(f"[ok  ] {label} ({e})")

print("\n=== Printed book ===")
b = OrderBook()
b.add_order("b1", BUY, 15.00, 100)
b.add_order("b2", BUY, 14.00, 50)
b.add_order("a1", SELL, 16.00, 100)
b.add_order("a2", SELL, 17.00, 50)
b.print_book()

print("\nAll Mock 5 checks passed.")
