from collections.abc import Sequence
from itertools import pairwise
from typing import NamedTuple

type Point = tuple[int, int]
type IndexedPoint = tuple[int, int, int]
type RankedPoint = tuple[int, int, int, int]


class ClosestPair(NamedTuple):
    first: int
    second: int
    squared_distance: int


def find(points: Sequence[Point]) -> ClosestPair | None:
    _validate(points)
    if len(points) < 2:
        return None
    by_x = sorted((x, y, i) for i, (x, y) in enumerate(points))
    duplicate = _closest_duplicate(by_x)
    if duplicate is not None:
        return ClosestPair(*duplicate, 0)
    by_y = sorted(
        ((x, y, i, rank) for rank, (x, y, i) in enumerate(by_x)), key=lambda point: (point[1], point[0], point[2])
    )
    return ClosestPair(*_solve(by_x, by_y, 0, len(by_x)))


def _validate(points: Sequence[Point]) -> None:
    limit = 10**9
    for point in points:
        if len(point) != 2 or any(
            isinstance(coordinate, bool) or not isinstance(coordinate, int) or abs(coordinate) > limit
            for coordinate in point
        ):
            raise ValueError("coordinates must be integers in [-10**9, 10**9]")


def _closest_duplicate(by_x: Sequence[IndexedPoint]) -> tuple[int, int] | None:
    duplicate: tuple[int, int] | None = None
    for left, right in pairwise(by_x):
        if left[:2] == right[:2]:
            indices = sorted((left[2], right[2]))
            candidate = (indices[0], indices[1])
            if duplicate is None or candidate < duplicate:
                duplicate = candidate
    return duplicate


def _squared_distance(left: IndexedPoint | RankedPoint, right: IndexedPoint | RankedPoint) -> int:
    return (left[0] - right[0]) ** 2 + (left[1] - right[1]) ** 2


def _solve(by_x: Sequence[IndexedPoint], by_y: list[RankedPoint], left: int, right: int) -> tuple[int, int, int]:
    n = right - left
    if n <= 3:
        best = (0, 0, 2**63 - 1)
        for i in range(left, right):
            for j in range(i + 1, right):
                candidate = (by_x[i][2], by_x[j][2], _squared_distance(by_x[i], by_x[j]))
                if candidate[0] > candidate[1]:
                    candidate = (candidate[1], candidate[0], candidate[2])
                if (candidate[2], candidate[0], candidate[1]) < (best[2], best[0], best[1]):
                    best = candidate
        return best
    mid = left + n // 2
    separator_x = by_x[mid][0]
    left_y = [point for point in by_y if point[3] < mid]
    right_y = [point for point in by_y if point[3] >= mid]
    best = min(
        _solve(by_x, left_y, left, mid), _solve(by_x, right_y, mid, right), key=lambda pair: (pair[2], pair[0], pair[1])
    )
    strip = [point for point in by_y if (point[0] - separator_x) ** 2 <= best[2]]
    for i, point in enumerate(strip):
        for other in strip[i + 1 : i + 8]:
            if (other[1] - point[1]) ** 2 > best[2]:
                break
            pair = sorted((point[2], other[2]))
            candidate = (pair[0], pair[1], _squared_distance(point, other))
            if (candidate[2], candidate[0], candidate[1]) < (best[2], best[0], best[1]):
                best = candidate
    return best
