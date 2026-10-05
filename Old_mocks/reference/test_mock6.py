"""
Verifies order_book_mock6.py — the Mock 6 escalations only.

The Mock 5 core is re-verified here too (the primer examples), since mock6 is standalone
and its matching loop must still behave identically.

Run:  python3 test_mock6.py
"""
from order_book_mock6 import OrderBook, BUY, SELL, to_cents


def check(label, got, want):
    status = "ok  " if got == want else "FAIL"
    print(f"[{status}] {label}\n        got  {got}\n        want {want}")
    assert got == want, label


print("=== Core still correct: the primer's partial-execution example ===")
b = OrderBook()
b.add_order("bid15", BUY, 15.00, 100)
b.add_order("bid14", BUY, 14.00, 50)
b.add_order("ask16", SELL, 16.00, 100)
b.add_order("ask17", SELL, 17.00, 50)
made = b.add_order("bob", SELL, 14.00, 200)
check("sweeps 100@15.00 then 50@14.00, leftover rests",
      [(t.qty, t.price) for t in made], [(100, 1500), (50, 1400)])
check("book after", b.snapshot(), ([], [(14.00, 50), (16.00, 100), (17.00, 50)]))

print("\n=== Part 1: spread ===")
b = OrderBook()
b.add_order("x1", BUY, 15.00, 100)
b.add_order("y1", SELL, 16.00, 100)
check("spread is 100 cents", b.spread(), 100)
b2 = OrderBook()
b2.add_order("only", BUY, 15.00, 100)
check("one-sided book has no spread", b2.spread(), None)
check("empty side best_ask is None", b2.best_ask(), None)

print("\n=== Part 2: depth and top-N levels ===")
b = OrderBook()
b.add_order("x1", BUY, 15.00, 100)
b.add_order("x2", BUY, 15.00, 50)
b.add_order("x3", BUY, 14.00, 50)
b.add_order("y1", SELL, 16.00, 100)
check("depth aggregates both orders at 15.00", b.depth(BUY, 15.00), 150)
check("depth of an empty price is 0", b.depth(BUY, 99.00), 0)
check("top 1 level per side", b.snapshot(levels=1), ([(15.00, 150)], [(16.00, 100)]))

print("\n=== Part 3: modify quantity — shrink keeps priority, grow loses it ===")
b = OrderBook()
b.add_order("first",  SELL, 16.00, 100)
b.add_order("second", SELL, 16.00, 100)
b.modify_qty("first", 50)
made = b.add_order("buyer", BUY, 16.00, 50)
check("shrunk order KEEPS its place at the front", [t.sell_id for t in made], ["first"])

b = OrderBook()
b.add_order("first",  SELL, 16.00, 100)
b.add_order("second", SELL, 16.00, 100)
b.modify_qty("first", 200)
made = b.add_order("buyer", BUY, 16.00, 100)
check("grown order went to the BACK; 'second' fills first",
      [t.sell_id for t in made], ["second"])
check("modify to 0 is a cancel", b.modify_qty("first", 0), True)
check("level empty afterwards", b.depth(SELL, 16.00), 0)
check("modify an unknown id is a no-op", b.modify_qty("ghost", 10), False)

print("\n=== Part 4: modify price — repricing into a cross trades immediately ===")
b = OrderBook()
b.add_order("resting_bid", BUY, 15.00, 100)
b.add_order("ask", SELL, 17.00, 100)
b.modify_price("ask", 15.00)
check("traded at the RESTING bid's price",
      [(t.qty, t.price) for t in b.trades], [(100, 1500)])
check("book empty afterwards", b.snapshot(), ([], []))

b = OrderBook()
b.add_order("a", SELL, 17.00, 100)
b.add_order("b", SELL, 16.00, 100)
b.modify_price("a", 16.00)
check("reprice with no cross just moves the order",
      b.snapshot()[1], [(16.00, 200)])
made = b.add_order("buyer", BUY, 16.00, 100)
check("repriced order is at the BACK of its new level", [t.sell_id for t in made], ["b"])

print("\n=== Part 5: market orders ===")
b = OrderBook()
b.add_order("a1", SELL, 16.00, 50)
b.add_order("a2", SELL, 17.00, 50)
made = b.add_market_order("mkt", BUY, 120)
check("sweeps both levels, each at its own resting price",
      [(t.qty, t.price) for t in made], [(50, 1600), (50, 1700)])
check("unfilled 20 does NOT rest — book is empty", b.snapshot(), ([], []))
check("market order into an empty book trades nothing",
      OrderBook().add_market_order("m", BUY, 100), [])

print("\n=== Part 6: IOC and FOK ===")
b = OrderBook()
b.add_order("a1", SELL, 16.00, 50)
made = b.add_ioc("ioc", BUY, 16.00, 100)
check("IOC fills what it can (50)", [(t.qty, t.price) for t in made], [(50, 1600)])
check("IOC remainder does not rest", b.snapshot(), ([], []))

b = OrderBook()
b.add_order("a1", SELL, 16.00, 50)
check("FOK for 100 against 50 available: nothing executes",
      b.add_fok("fok", BUY, 16.00, 100), [])
check("FOK left the book completely untouched", b.depth(SELL, 16.00), 50)
check("FOK for 50 fills completely",
      [(t.qty, t.price) for t in b.add_fok("fok2", BUY, 16.00, 50)], [(50, 1600)])

b = OrderBook()
b.add_order("a1", SELL, 16.00, 50)
b.add_order("a2", SELL, 17.00, 50)
check("FOK counts only levels that actually cross its limit (50, not 100)",
      b.add_fok("fok3", BUY, 16.00, 100), [])

print("\n=== Part 7: self-trade prevention ===")
b = OrderBook(self_trade_policy="cancel_resting")
b.add_order("mine",   SELL, 16.00, 100, trader="jim")
b.add_order("theirs", SELL, 16.00, 100, trader="pat")
made = b.add_order("mybuy", BUY, 16.00, 100, trader="jim")
check("skips my own resting offer, fills against pat's",
      [t.sell_id for t in made], ["theirs"])
check("my own offer was cancelled, not left resting", b.depth(SELL, 16.00), 0)

b = OrderBook(self_trade_policy="cancel_incoming")
b.add_order("mine", SELL, 16.00, 100, trader="jim")
made = b.add_order("mybuy", BUY, 16.00, 100, trader="jim")
check("cancel_incoming: no trade at all", made, [])
check("resting order survives untouched", b.depth(SELL, 16.00), 100)

print("\n=== Part 8: edge cases ===")
b = OrderBook()
for label, fn in [
    ("zero quantity rejected",        lambda: b.add_order("z", BUY, 15.00, 0)),
    ("negative quantity rejected",    lambda: b.add_order("n", BUY, 15.00, -5)),
    ("negative price rejected",       lambda: b.add_order("p", BUY, -1.00, 10)),
    ("market order qty 0 rejected",   lambda: b.add_market_order("m", BUY, 0)),
]:
    try:
        fn()
        print(f"[FAIL] {label} — no error raised"); raise SystemExit(1)
    except ValueError as e:
        print(f"[ok  ] {label} ({e})")

b.add_order("dup", BUY, 15.00, 100)
try:
    b.add_order("dup", BUY, 15.00, 100)
    print("[FAIL] duplicate id — no error raised"); raise SystemExit(1)
except ValueError as e:
    print(f"[ok  ] duplicate order id rejected ({e})")

b = OrderBook()
b.add_order("f", BUY, 0.10, 100)
b.add_order("g", BUY, 0.20, 100)
check("integer cents: 0.1/0.2 stored exactly", sorted(b.level_qty[BUY]), [10, 20])

print("\nAll Mock 6 checks passed.")
