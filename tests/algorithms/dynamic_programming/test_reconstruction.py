from itertools import combinations, pairwise, product

from algorithms.dynamic_programming import (
    edit_distance,
    knapsack_01,
    longest_common_subsequence,
    longest_increasing_subsequence,
)


def subsets(n):
    for k in range(n + 1):
        yield from combinations(range(n), k)


def is_subsequence(seq, text):
    it = iter(text)
    return all(any(x == y for y in it) for x in seq)


def test_knapsack_reconstruction_against_exhaustive_subsets():
    items = list(product((0, 1), (-1, 0, 2)))
    for n in range(5):
        for selected in product(items, repeat=n):
            weights = [w for w, _ in selected]
            values = [v for _, v in selected]
            for cap in range(3):
                val, indices = knapsack_01.solve(weights, values, cap)
                opt = max(sum(values[i] for i in s) for s in subsets(n) if sum(weights[i] for i in s) <= cap)
                assert isinstance(indices, list)
                assert indices == sorted(set(indices))
                assert all(0 <= i < n for i in indices)
                assert sum(weights[i] for i in indices) <= cap
                assert sum(values[i] for i in indices) == val == opt


def test_lis_reconstruction_against_exhaustive_subsequences():
    for n in range(7):
        for values in product((-1, 0, 1), repeat=n):
            seq, indices = longest_increasing_subsequence.solve(values)
            opt = max(len(s) for s in subsets(n) if all(values[i] < values[j] for i, j in pairwise(s)))
            assert isinstance(seq, list) and isinstance(indices, list)
            assert indices == sorted(set(indices))
            assert all(0 <= i < n for i in indices)
            assert seq == [values[i] for i in indices]
            assert all(x < y for x, y in pairwise(seq))
            assert len(seq) == opt


def test_lcs_reconstruction_against_exhaustive_subsequences():
    strings = ["".join(s) for n in range(5) for s in product("ab", repeat=n)]
    for a, b in product(strings, repeat=2):
        ans = longest_common_subsequence.solve(a, b)
        opt = max(len(s) for s in subsets(len(a)) if is_subsequence([a[i] for i in s], b))
        assert isinstance(ans, str)
        assert is_subsequence(ans, a) and is_subsequence(ans, b)
        assert len(ans) == opt


def test_edit_reconstruction_against_exhaustive_alignments():
    def cost(a, b):
        if not a or not b:
            return len(a) + len(b)
        return min((a[0] != b[0]) + cost(a[1:], b[1:]), 1 + cost(a[1:], b), 1 + cost(a, b[1:]))

    strings = ["".join(s) for n in range(4) for s in product("ab", repeat=n)]
    for a, b in product(strings, repeat=2):
        val, edits = edit_distance.align(a, b)
        assert isinstance(edits, list)
        assert "".join(e.source for e in edits if e.source is not None) == a
        assert "".join(e.target for e in edits if e.target is not None) == b
        for e in edits:
            if e.source is None:
                assert e.kind == "insert" and e.target is not None
            elif e.target is None:
                assert e.kind == "delete"
            else:
                assert e.kind == ("match" if e.source == e.target else "replace")
        assert sum(e.kind != "match" for e in edits) == val == cost(a, b)
