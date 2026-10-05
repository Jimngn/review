"""Mock 5 - Order Book. My attempt. Part 1: represent order + book."""
from collections import deque
from dataclasses import dataclass
from itertools import count

BUY, SELL = "BUY", "SELL"


@dataclass
class Order:
    order_id : str
    side: str
    price: int
    qty: int
    seq: int = 0 #since timestamp have finite resolution and can be tied
    active: bool = True
    
class Book:
    def __init__(self):
        self.levels = {BUY: {}, SELL: {}}
        self.level_qty = {BUY: {}, SELL: {}}
        self.orders = {} #maps order id -> order
        self.trades = []
        self.seq = count()
                

    def add_order(self, order_id, side, price, qty):
        """Part 1: just rest it. No matching yet."""
        order = Order(order_id, side, price, qty, seq = next(self.seq))
        self.orders[order_id] = order
        
        book_side = self.levels[side]
        if price not in book_side:
            book_side[price] = deque()
        book_side[price].append(order)
            
        qty_side = self.level_qty[side]
        if price not in qty_side:
            qty_side[price] = qty
        else:
            qty_side[price] += qty
                          

    def best_bid(self):
        if not self.levels[BUY]:
            return None
        return max(self.levels[BUY])

    def best_ask(self):
        if not self.levels[SELL]:
            return None
        return min(self.levels[SELL])

book1 = Book()
book1.add_order("order1", BUY, 1500, 1)
book1.add_order("order2", SELL, 1600, 1)

