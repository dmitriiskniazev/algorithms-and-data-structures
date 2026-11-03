from collections.abc import Mapping
from heapq import heapify, heappop, heappush
from itertools import count

type Tree = str | tuple[Tree, Tree]


def build_codes(frequencies: Mapping[str, int]) -> dict[str, str]:
    if any(not isinstance(symbol, str) for symbol in frequencies):
        raise TypeError("symbols must be strings")
    for frequency in frequencies.values():
        if not isinstance(frequency, int) or frequency <= 0:
            raise ValueError("frequencies must be positive integers")
    if not frequencies:
        return {}
    if len(frequencies) == 1:
        symbol = next(iter(frequencies))
        return {symbol: "0"}

    serial = count()
    # Heap entries are (weight, serial, tree); serial prevents comparing trees.
    heap: list[tuple[int, int, Tree]] = [(frequency, next(serial), symbol) for symbol, frequency in frequencies.items()]
    heapify(heap)
    while len(heap) > 1:
        left_weight, _, left = heappop(heap)
        right_weight, _, right = heappop(heap)
        heappush(heap, (left_weight + right_weight, next(serial), (left, right)))

    codes: dict[str, str] = {}
    stack: list[tuple[Tree, str]] = [(heap[0][2], "")]
    while stack:
        tree, prefix = stack.pop()
        if isinstance(tree, str):
            codes[tree] = prefix
            continue
        left, right = tree
        stack.append((right, prefix + "1"))
        stack.append((left, prefix + "0"))
    return codes
