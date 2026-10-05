"""
Reference matching engine for MOCK 6 — the escalations on top of the Mock 5 core.

This file is STANDALONE: it repeats the Mock 5 core so you can read it top to bottom.
If you only want to understand the core, read order_book_mock5.py instead — it is the
same engine with everything below stripped out.

Every Mock 6 addition is marked with a `# +++ MOCK 6 +++` banner, so you can see exactly
what each escalation cost:

    Part 1  best bid / best offer, spread        -> spread()            (+3 lines)
    Part 2  depth at a price, top-N levels       -> depth(), snapshot(levels=)
    Part 3  modify quantity                      -> modify_qty()
    Part 4  modify price                         -> modify_price()
    Part 5  market orders                        -> add_market_order()
    Part 6  immediate-or-cancel, fill-or-kill    -> add_ioc(), add_fok(), _available_qty()
    Part 7  self-trade prevention                -> trader field, policy check in _match
    Part 8  edge cases                           -> validation in add_order()

The thing to notice: Parts 4, 5 and 6 are nearly free BECAUSE the Mock 5 core kept
"matching" and "resting" as two separate steps. A reprice is cancel + add_order. An IOC is
add_order minus the _rest() call. If your Mock 5 design fused those two steps, every one of
these escalations becomes a rewrite. That is the whole point of the mock.
"""

from collections import deque
from dataclasses import dataclass
from itertools import count

BUY = "BUY"
SELL = "SELL"


def to_cents(dollars):
    return int(round(dollars * 100))


def to_dollars(cents):
    return cents / 100


@dataclass
class Order:
    order_id: str
    side: str
    price: int          # cents; None for a market order     # +++ MOCK 6 +++ (None case)
    qty: int
    trader: str = None  # +++ MOCK 6 +++ Part 7, for self-trade prevention
    seq: int = 0
    active: bool = True


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
    def __init__(self, self_trade_policy="cancel_resting"):   # +++ MOCK 6 +++ Part 7
        self.levels = {BUY: {}, SELL: {}}
        self.level_qty = {BUY: {}, SELL: {}}
        self.orders = {}
        self.trades = []
        self._seq = count()
        self.self_trade_policy = self_trade_policy

    # ------------------------------------------------------------------ reporting

    def best_bid(self):
        return max(self.levels[BUY]) if self.levels[BUY] else None

    def best_ask(self):
        return min(self.levels[SELL]) if self.levels[SELL] else None

    # +++ MOCK 6 +++ Part 1 -------------------------------------------------------
    def spread(self):
        """None when either side is empty — a one-sided book has no spread. Returning 0
        or a huge number here is the trap; 0 would also look like a real price."""
        bid, ask = self.best_bid(), self.best_ask()
        if bid is None or ask is None:
            return None
        return ask - bid

    # +++ MOCK 6 +++ Part 2 -------------------------------------------------------
    def depth(self, side, price):
        """Total resting quantity at one price. O(1) because level_qty is maintained on
        every rest, fill and cancel — rather than summing the queue each time."""
        return self.level_qty[side].get(to_cents(price), 0)

    def snapshot(self, levels=None):
        """Aggregated book, best-first. `levels` caps how many price levels per side.

        +++ MOCK 6 +++ the `levels` cap is new. Note out loud that "top N levels" is the
        top-k problem again: sorting all levels is O(P log P), and if P were large you'd
        use heapq.nlargest for O(P log k), or keep levels in a sorted structure.
        """
        bids = sorted(self.level_qty[BUY].items(), reverse=True)
        asks = sorted(self.level_qty[SELL].items())
        if levels is not None:
            bids, asks = bids[:levels], asks[:levels]
        to_rows = lambda rows: [(to_dollars(p), q) for p, q in rows]
        return to_rows(bids), to_rows(asks)

    def print_book(self):
        bids, asks = self.snapshot()
        for price, qty in reversed(asks):
            print(f"ASK  ${price:>7.2f}  {qty:>5}")
        print("-" * 22)
        for price, qty in bids:
            print(f"BID  ${price:>7.2f}  {qty:>5}")

    # ------------------------------------------------------------ internal bookkeeping

    def _rest(self, order):
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
        queue = self.levels[side].get(price)
        while queue and not queue[0].active:
            queue.popleft()
        if not queue:
            self.levels[side].pop(price, None)
            self.level_qty[side].pop(price, None)
            return None
        return queue[0]

    def _crosses(self, side, limit_price, opposite_best):
        if opposite_best is None:
            return False
        # +++ MOCK 6 +++ Part 5: a market order has no limit, so it crosses anything.
        # Representing "no limit" as None lets market orders reuse the SAME matching loop
        # instead of needing a second code path.
        if limit_price is None:
            return True
        return limit_price >= opposite_best if side == BUY else limit_price <= opposite_best

    # +++ MOCK 6 +++ Part 6 -------------------------------------------------------
    def _available_qty(self, side, limit_price):
        """How much WOULD fill, without executing anything. Fill-or-kill needs this because
        you cannot un-print a trade after discovering there wasn't enough size."""
        other = SELL if side == BUY else BUY
        prices = (sorted(self.level_qty[other]) if side == BUY
                  else sorted(self.level_qty[other], reverse=True))
        total = 0
        for price in prices:
            if not self._crosses(side, limit_price, price):
                break                      # levels are ordered, so the first miss ends it
            total += self.level_qty[other][price]
        return total

    # ------------------------------------------------------------------- matching

    def _match(self, incoming):
        other = SELL if incoming.side == BUY else BUY
        made = []

        while incoming.qty > 0:
            best = self.best_ask() if incoming.side == BUY else self.best_bid()
            if not self._crosses(incoming.side, incoming.price, best):
                break

            resting = self._front(other, best)
            if resting is None:
                continue

            # +++ MOCK 6 +++ Part 7: self-trade prevention.
            # Trading with yourself prints a real trade at a price you chose with no change
            # in your position — wash trading. It fakes volume and can paint a misleading
            # price, which is a regulatory problem, not just an aesthetic one.
            if incoming.trader is not None and resting.trader == incoming.trader:
                if self.self_trade_policy == "cancel_resting":
                    self.cancel(resting.order_id)
                    continue                      # keep matching further down the book
                elif self.self_trade_policy == "cancel_incoming":
                    incoming.qty = 0
                    break

            traded = min(incoming.qty, resting.qty)

            # Trade price is the RESTING order's price. Unchanged from Mock 5.
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

            if resting.qty == 0:
                resting.active = False
                self.orders.pop(resting.order_id, None)
                queue = self.levels[other].get(resting.price)
                if queue and queue[0] is resting:
                    queue.popleft()

        return made

    # -------------------------------------------------------------- order entry

    def add_order(self, order_id, side, price, qty, trader=None):
        """Limit order: match what crosses, rest the remainder."""
        # +++ MOCK 6 +++ Part 8: validate at the boundary, so the matching loop can trust
        # its input. A zero-quantity order that reached _match would trade 0 forever and
        # never terminate; a negative quantity would corrupt every level total.
        if qty <= 0:
            raise ValueError(f"quantity must be positive, got {qty}")
        if price is not None and price <= 0:
            raise ValueError(f"price must be positive, got {price}")
        if order_id in self.orders:
            raise ValueError(f"duplicate order id {order_id!r}")

        order = Order(order_id, side, to_cents(price), qty, trader, next(self._seq))
        made = self._match(order)
        if order.qty > 0:
            self._rest(order)
        return made

    # +++ MOCK 6 +++ Part 5 -------------------------------------------------------
    def add_market_order(self, order_id, side, qty, trader=None):
        """No limit price. Sweeps until filled or the book runs dry; the remainder is
        CANCELLED, never rested — a resting order needs a price, and this one has none."""
        if qty <= 0:
            raise ValueError(f"quantity must be positive, got {qty}")
        order = Order(order_id, side, None, qty, trader, next(self._seq))
        return self._match(order)          # note: no _rest() call

    # +++ MOCK 6 +++ Part 6 -------------------------------------------------------
    def add_ioc(self, order_id, side, price, qty, trader=None):
        """Immediate-or-cancel: the limit path minus the _rest() call. One line of
        difference, because Mock 5 kept matching and resting separate."""
        order = Order(order_id, side, to_cents(price), qty, trader, next(self._seq))
        return self._match(order)

    def add_fok(self, order_id, side, price, qty, trader=None):
        """Fill-or-kill: all or nothing. Needs a pre-check pass — you can't start matching
        and bail halfway, because the trades you already printed have happened."""
        limit = to_cents(price)
        if self._available_qty(side, limit) < qty:
            return []                      # kill: nothing executes at all
        order = Order(order_id, side, limit, qty, trader, next(self._seq))
        return self._match(order)

    # ----------------------------------------------------------------- cancel

    def cancel(self, order_id):
        order = self.orders.pop(order_id, None)
        if order is None:
            return False
        order.active = False
        self._reduce_level(order.side, order.price, order.qty)
        return True

    # +++ MOCK 6 +++ Part 3 -------------------------------------------------------
    def modify_qty(self, order_id, new_qty):
        """SHRINKING keeps queue position; GROWING goes to the back.

        Say the reasoning before the code: giving up size costs the traders behind you
        nothing, so there's no reason to punish it. But if growing kept your place, you'd
        post a 1-lot early to camp at the front of the queue and inflate it later — that
        gaming is exactly what the rule prevents.
        """
        order = self.orders.get(order_id)
        if order is None:
            return False
        if new_qty <= 0:
            return self.cancel(order_id)            # qty 0 means cancel
        if new_qty < order.qty:
            self._reduce_level(order.side, order.price, order.qty - new_qty)
            order.qty = new_qty                     # stays where it is in the deque
            return True
        side, price, trader = order.side, order.price, order.trader
        self.cancel(order_id)
        self._rest(Order(order_id, side, price, new_qty, trader, next(self._seq)))
        return True

    # +++ MOCK 6 +++ Part 4 -------------------------------------------------------
    def modify_price(self, order_id, new_price):
        """A reprice is just a cancel plus an add. Routing it through add_order means a
        repriced order that now CROSSES trades immediately, with no new matching code.

        Watch the ordering: cancel BEFORE re-adding, or the duplicate-id guard fires.
        """
        order = self.orders.get(order_id)
        if order is None:
            return False
        side, qty, trader = order.side, order.qty, order.trader
        self.cancel(order_id)
        self.add_order(order_id, side, new_price, qty, trader)
        return True
