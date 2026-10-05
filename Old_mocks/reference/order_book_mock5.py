"""
Reference matching engine for MOCK 5 ONLY — the order book core.

This file deliberately contains NOTHING from Mock 6. No market orders, no IOC/FOK, no
modify, no self-trade prevention. Just the six parts of Mock 5, in order:

    Part 1  represent an order and the book      -> Order, OrderBook.__init__
    Part 2  print the book                       -> snapshot, print_book
    Part 3  matching                             -> _match, add_order
    Part 4  partial fills and sweeping           -> (falls out of _match's while loop)
    Part 5  cancel                               -> cancel
    Part 6  complexity                           -> see the notes at the bottom

Mock 6's extensions live in order_book_mock6.py, which is a separate, self-contained file.

-------------------------------------------------------------------------------
THE FOUR DESIGN DECISIONS, AND WHAT TO SAY ABOUT EACH
-------------------------------------------------------------------------------
1. PRICES ARE INTEGER CENTS.
   Floats do not compare exactly (0.1 + 0.2 != 0.3). An exchange's core operation is
   comparing prices for equality and ordering, so a rounding error means two orders
   silently fail to cross. Store cents; format dollars only for display.

2. EACH SIDE IS A DICT: price -> deque of resting orders.
   The dict gives O(1) access to a price level. The deque gives time priority within the
   level: append at the back, pop from the front, both O(1). A list would make pop(0) O(n),
   so a busy price level would degrade quadratically.

3. BEST PRICE IS max(bids) / min(asks), which is O(P) in distinct price levels.
   Say this cost out loud, then name the upgrade: cache the best price and update it
   incrementally (O(1) reads), or use a heap / sorted container (O(log P)).

4. CANCEL IS O(1) VIA LAZY DELETION.
   Flag the order inactive and subtract its quantity from the level total. Matching skips
   the tombstone when it reaches it. The production alternative is a doubly-linked list per
   price level plus an id -> node map, which unlinks in O(1) with no tombstones left behind.
"""

from collections import deque
from dataclasses import dataclass
from itertools import count

BUY = "BUY"
SELL = "SELL"


def to_cents(dollars):
    """$15.00 -> 1500. Round, don't truncate: int(15.00 * 100) can land on 1499."""
    return int(round(dollars * 100))


def to_dollars(cents):
    return cents / 100


# ---------------------------------------------------------------- Part 1: the data model

@dataclass
class Order:
    order_id: str
    side: str
    price: int      # cents
    qty: int
    seq: int = 0    # arrival sequence — the real tiebreaker for time priority.
                    # Timestamps have finite resolution and can tie; a monotonic
                    # sequence number assigned on receipt cannot.
    active: bool = True   # False once cancelled or fully filled (see cancel())


@dataclass
class Trade:
    price: int
    qty: int
    buy_id: str
    sell_id: str

    def __str__(self):
        return (f"TRADE {self.qty} @ ${to_dollars(self.price):.2f} "
                f"(buy {self.buy_id} / sell {self.sell_id})")


class OrderBook:
    def __init__(self):
        # side -> {price: deque[Order]}   — the resting orders, in arrival order per price
        self.levels = {BUY: {}, SELL: {}}
        # side -> {price: total ACTIVE qty}  — kept in step so depth is O(1) and so an
        # emptied level can be deleted immediately (otherwise best_bid() would happily
        # return a price level containing nothing but cancelled orders)
        self.level_qty = {BUY: {}, SELL: {}}
        self.orders = {}          # order_id -> Order, for O(1) cancel. Resting orders only.
        self.trades = []
        self._seq = count()

    # ------------------------------------------------------- Part 2: reporting the book

    def best_bid(self):
        """Highest bid price, or None if there are no bids. O(P)."""
        return max(self.levels[BUY]) if self.levels[BUY] else None

    def best_ask(self):
        """Lowest offer price, or None if there are no offers. O(P)."""
        return min(self.levels[SELL]) if self.levels[SELL] else None

    def snapshot(self):
        """Aggregated levels, best-first: ([(price, qty), ...] bids, [...] asks).

        Aggregate by price level — the point of a book display is total size available at
        each price, not one row per order.
        """
        bids = sorted(self.level_qty[BUY].items(), reverse=True)   # best = highest first
        asks = sorted(self.level_qty[SELL].items())                # best = lowest first
        to_rows = lambda rows: [(to_dollars(p), q) for p, q in rows]
        return to_rows(bids), to_rows(asks)

    def print_book(self):
        """Offers above, bids below, so the two best prices meet in the middle at the
        spread — the layout every real book display uses."""
        bids, asks = self.snapshot()
        for price, qty in reversed(asks):      # worst offer on top, best offer just above the line
            print(f"ASK  ${price:>7.2f}  {qty:>5}")
        print("-" * 22)
        for price, qty in bids:                # best bid just below the line
            print(f"BID  ${price:>7.2f}  {qty:>5}")

    # ------------------------------------------------------------ internal bookkeeping

    def _rest(self, order):
        """Put an order on the book at the back of its price level's queue."""
        self.levels[order.side].setdefault(order.price, deque()).append(order)
        qty = self.level_qty[order.side]
        qty[order.price] = qty.get(order.price, 0) + order.qty
        self.orders[order.order_id] = order

    def _reduce_level(self, side, price, amount):
        qty = self.level_qty[side]
        qty[price] -= amount
        if qty[price] <= 0:
            del qty[price]
            del self.levels[side][price]

    def _front(self, side, price):
        """Oldest live order at a price, discarding cancelled tombstones as we reach them.
        Returns None if the level turned out to be entirely dead."""
        queue = self.levels[side].get(price)
        while queue and not queue[0].active:
            queue.popleft()
        if not queue:
            self.levels[side].pop(price, None)
            self.level_qty[side].pop(price, None)
            return None
        return queue[0]

    def _crosses(self, side, limit_price, opposite_best):
        """A bid crosses an offer when bid >= offer. Note >=, not > : equal prices trade."""
        if opposite_best is None:
            return False
        return limit_price >= opposite_best if side == BUY else limit_price <= opposite_best

    # ------------------------------------------- Parts 3 and 4: matching and partial fills

    def _match(self, incoming):
        """Execute `incoming` against the book, mutating incoming.qty down as it fills.

        In plain English, which is how to narrate it in the interview:
        "While the incoming order still has quantity and the best opposite price crosses my
         limit, take the oldest order at that best price, trade the smaller of the two
         quantities AT THE RESTING ORDER'S PRICE, and remove the resting order if it's
         exhausted."

        Part 4 needs no extra code: the while loop re-picks the best price every pass, so
        sweeping several levels is automatic, and whatever quantity is left over is simply
        still sitting in incoming.qty when the loop exits.
        """
        other = SELL if incoming.side == BUY else BUY
        made = []

        while incoming.qty > 0:
            best = self.best_ask() if incoming.side == BUY else self.best_bid()
            if not self._crosses(incoming.side, incoming.price, best):
                break                       # no cross -> done matching

            resting = self._front(other, best)
            if resting is None:
                continue                    # that level was all tombstones; re-pick the best

            traded = min(incoming.qty, resting.qty)

            # THE RULE PEOPLE GET WRONG: the trade happens at the RESTING order's price,
            # not the incoming order's. Jane Street's primer states this explicitly — the
            # trade occurs "at the price of the order that was already listed".
            trade = Trade(
                price=resting.price,
                qty=traded,
                buy_id=incoming.order_id if incoming.side == BUY else resting.order_id,
                sell_id=resting.order_id if incoming.side == BUY else incoming.order_id,
            )
            made.append(trade)
            self.trades.append(trade)

            incoming.qty -= traded
            resting.qty -= traded
            self._reduce_level(other, resting.price, traded)

            if resting.qty == 0:            # resting order fully consumed -> off the book
                resting.active = False
                self.orders.pop(resting.order_id, None)
                queue = self.levels[other].get(resting.price)
                if queue and queue[0] is resting:
                    queue.popleft()

        return made

    def add_order(self, order_id, side, price, qty):
        """A limit order: match whatever crosses, then rest the remainder."""
        if qty <= 0:
            raise ValueError(f"quantity must be positive, got {qty}")
        if price <= 0:
            raise ValueError(f"price must be positive, got {price}")
        if order_id in self.orders:
            raise ValueError(f"duplicate order id {order_id!r}")

        order = Order(order_id, side, to_cents(price), qty, next(self._seq))
        made = self._match(order)
        if order.qty > 0:
            self._rest(order)               # Part 4: the leftover rests on the book
        return made

    # -------------------------------------------------------------------- Part 5: cancel

    def cancel(self, order_id):
        """O(1). Returns False — not an exception — for an unknown id, a double cancel, or
        an order that was already fully filled. The caller often cannot tell those apart
        (they may have raced with a fill), so they are all the same harmless no-op."""
        order = self.orders.pop(order_id, None)
        if order is None:
            return False
        order.active = False                        # tombstone; matching skips it later
        self._reduce_level(order.side, order.price, order.qty)
        return True


# -------------------------------------------------------------------------------
# PART 6 — THE COMPLEXITY ANSWERS, READY TO RECITE
#
#   n = orders consumed by one match, P = distinct price levels, m = orders at one level
#
#   add_order, no cross  O(P)   finding the best opposite price dominates
#                               -> O(1) with a cached best price, O(log P) with a heap
#   add_order, crossing  O(n+P) proportional to how many resting orders it eats
#   cancel               O(1)   id -> order map + lazy deletion
#   best_bid / best_ask  O(P)   -> O(1) cached, O(log P) heap
#   snapshot             O(P log P) because it sorts the levels
#
# THE AMORTIZATION POINT, worth making unprompted: one order might sweep a thousand resting
# orders, but every resting order can only ever be consumed ONCE in its lifetime. So the
# cost is amortized across all the orders that ever rested — it is not quadratic.
#
# "A MILLION ORDERS A SECOND?" — three answers to have ready:
#   1. Integer cents, and fixed-size arrays indexed by price tick instead of hash maps
#      (real books only trade in a narrow band around the touch).
#   2. Pre-allocated order objects / object pools, to keep allocation out of the hot path.
#   3. Drop the max()/min() scan entirely by caching the best price incrementally.
#   ...and, honestly: "I'd profile before guessing."
# -------------------------------------------------------------------------------
