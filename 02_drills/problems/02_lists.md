# Drill Set 2 — Lists

Solve each without looking at `../solutions/02_lists.md`.

## 1. Second largest
Write `second_largest(nums)` that returns the second-largest **distinct** value in the list.
Assume the list has at least 2 distinct values.
```
second_largest([5, 1, 4, 4, 2]) -> 4
second_largest([1, 2])          -> 1
```

## 2. Remove duplicates, preserve order
Write `dedupe(items)` that returns a new list with duplicates removed, keeping the first
occurrence of each value and the original order.
```
dedupe([1, 2, 2, 3, 1, 4]) -> [1, 2, 3, 4]
```

## 3. Flatten a list of lists (one level deep)
Write `flatten(list_of_lists)` that combines a list of lists into a single flat list.
```
flatten([[1, 2], [3], [], [4, 5]]) -> [1, 2, 3, 4, 5]
```

## 4. Running total
Write `running_total(nums)` that returns a new list where each element is the sum of all
elements up to and including that position.
```
running_total([1, 2, 3, 4]) -> [1, 3, 6, 10]
```

## 5. Rotate a list
Write `rotate(lst, k)` that rotates the list to the right by `k` positions.
```
rotate([1, 2, 3, 4, 5], 2) -> [4, 5, 1, 2, 3]
```

## 6. Merge two sorted lists
Write `merge_sorted(a, b)` that takes two already-sorted lists and returns one sorted list
containing all elements of both. (You may use `sorted(a + b)` as a fallback if you get stuck
on the manual two-pointer approach — but try the manual approach first, it's a very common
interview shape.)
```
merge_sorted([1, 3, 5], [2, 4, 6]) -> [1, 2, 3, 4, 5, 6]
```
