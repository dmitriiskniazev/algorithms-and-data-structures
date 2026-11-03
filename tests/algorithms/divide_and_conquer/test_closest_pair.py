from random import Random

import pytest

from algorithms.divide_and_conquer import closest_pair


def brute_force(points: list[tuple[int, int]]) -> closest_pair.ClosestPair | None:
    candidates = [
        ((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2, i, j)
        for i in range(len(points))
        for j in range(i + 1, len(points))
    ]
    if not candidates:
        return None
    distance, first, second = min(candidates)
    return closest_pair.ClosestPair(first, second, distance)


@pytest.mark.parametrize(
    ("points", "expected"),
    [
        ([], None),
        ([(5, -7)], None),
        ([(0, 0), (0, 0)], closest_pair.ClosestPair(0, 1, 0)),
        ([(9, 2), (-4, 3), (9, 2), (9, 2)], closest_pair.ClosestPair(0, 2, 0)),
        ([(-3, -4), (-3, 0), (2, -4)], closest_pair.ClosestPair(0, 1, 16)),
        ([(0, 0), (2, 0), (1, 1), (1, -1)], closest_pair.ClosestPair(0, 2, 2)),
        ([(-(10**9), -(10**9)), (10**9, 10**9)], closest_pair.ClosestPair(0, 1, 8 * 10**18)),
    ],
)
def test_examples(points: list[tuple[int, int]], expected: closest_pair.ClosestPair | None) -> None:
    assert closest_pair.find(points) == expected


@pytest.mark.parametrize("point", [(10**9 + 1, 0), (0, -(10**9 + 1)), (True, 0), (1.5, 1)])
def test_rejects_invalid_coordinates_even_for_short_input(point: tuple[object, object]) -> None:
    with pytest.raises(ValueError):
        closest_pair.find([point])  # type: ignore[list-item]


def test_randomized_differential_against_brute_force() -> None:
    rng = Random(0xC105E57)
    for size in range(2, 35):
        for _ in range(25):
            points = [(rng.randrange(-20, 21), rng.randrange(-20, 21)) for _ in range(size)]
            assert closest_pair.find(points) == brute_force(points)


def test_large_same_x_and_equal_x_split() -> None:
    points = [(7, y) for y in [30, 2, 19, -10, 8, 100, 1, 45, -40, 6, 11, 3]]
    assert closest_pair.find(points) == brute_force(points)
