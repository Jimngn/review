# Mock 3 — Trade Aggregation

Not a directly reported question, but a natural extension of the guide's dictionary material
into the same trading-desk framing the reported questions used — practice this shape too.

## Part 1
> "You're given a list of trades, each a tuple of `(symbol, price, quantity)`. Write a
> function that returns the total quantity traded per symbol."
```
trades = [("AAPL", 150.0, 10), ("GOOG", 2800.0, 2), ("AAPL", 151.5, 5)]
```
Write `total_quantity_by_symbol(trades)`, returning a dict like `{"AAPL": 15, "GOOG": 2}`.

Questions worth asking before coding: can the same symbol appear many times? Can quantity be
negative (e.g. representing a sell)? Decide an assumption and state it out loud if the
interviewer doesn't specify.

## Part 2
> "Now find the symbol with the highest total *dollar value* traded (price × quantity,
> summed per symbol), not just quantity."

Write `symbol_with_highest_value(trades)`.

## Part 3
> "Suppose some trades are erroneous — a quantity of zero or negative should be excluded
> entirely from your totals. Adjust your function."

Update your Part 1 or Part 2 solution to filter these out. Where exactly does the filter
belong in your loop, and why there?

## Part 4 — manual trace
Trace `symbol_with_highest_value` by hand for:
```
trades = [("AAPL", 100.0, 3), ("GOOG", 50.0, 10), ("AAPL", 100.0, 4)]
```
Write out the running dict state after each trade is processed, before computing the max.

## Part 5 — a twist on the data shape
> "Now imagine the trades come in as raw text lines instead of tuples, one trade per line,
> formatted `SYMBOL,PRICE,QUANTITY`. Adapt your solution."
```python
raw = """AAPL,100.0,3
GOOG,50.0,10
AAPL,100.0,4"""
```
What has to change, and what stays exactly the same?
