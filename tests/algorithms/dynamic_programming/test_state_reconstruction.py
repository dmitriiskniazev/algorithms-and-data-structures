import random
import re
from importlib import import_module
from itertools import pairwise
from pathlib import Path

import pytest

MODULES = {
    "knapsack": ("knapsack_01", "0/1-рюкзак"),
    "lcs": ("longest_common_subsequence", "Наибольшая общая подпоследовательность"),
    "edit": ("edit_distance", "Расстояние редактирования"),
    "schedule": ("weighted_interval_scheduling", "Взвешенное расписание интервалов"),
    "lis": ("longest_increasing_subsequence", "Наибольшая возрастающая подпоследовательность"),
    "matrix": ("matrix_chain_order", "Оптимальное умножение цепочки матриц"),
}


@pytest.mark.parametrize("kind", MODULES)
def test_separate_forward_passes_and_both_reconstructions(kind):
    name, title = MODULES[kind]
    module = import_module(f"algorithms.dynamic_programming.{name}")
    build_values = module.build_table
    optimize = module.build_parents
    restore_values = module.restore_from_table
    restore_parents = module.restore_from_parents
    text = (Path(__file__).resolve().parents[3] / "docs/algorithms/dynamic-programming.md").read_text()
    section = text.split(f"## {title}\n", 1)[1].split("\n## ", 1)[0]
    snippets = re.findall(r"```python\n(.*?)\n```", section, re.DOTALL)
    assert len(snippets) == 2
    rng = random.Random(42)
    for _ in range(200):
        if kind == "knapsack":
            n = rng.randrange(8)
            weights = [rng.randrange(4) for _ in range(n)]
            values = [rng.randrange(-3, 5) for _ in range(n)]
            cap = rng.randrange(6)
            args = weights, values, cap
            dp = build_values(*args)
            val_with_parents, parents = optimize(*args)
            assert val_with_parents == dp[-1][cap]
            ans = restore_values(weights, cap, dp)
            assert restore_parents(weights, cap, parents) == ans
            env = {"weights": weights, "values": values, "cap": cap}
            expected = dp[-1][cap], ans
        elif kind in ("lcs", "edit"):
            a, b = ("".join(rng.choices("ab", k=rng.randrange(6))) for _ in range(2))
            dp = build_values(a, b)
            val_with_parents, parents = optimize(a, b)
            assert val_with_parents == dp[-1][-1]
            ans = restore_values(a, b, dp)
            assert restore_parents(a, b, parents) == ans
            env = {"A": a, "B": b, "X": a, "Y": b}
            expected = dp[-1][-1], ans
            if kind == "edit":
                assert module.compute(a, b) == expected[0]
        elif kind == "schedule":
            intervals = []
            for _ in range(rng.randrange(8)):
                start = rng.randrange(5)
                intervals.append((start, start + rng.randrange(4), rng.randrange(-3, 5)))
            jobs, empty = module.prepare_jobs(intervals)
            dp, prev = build_values(jobs)
            val_with_parents, parents = optimize(jobs)
            assert val_with_parents == dp[-1]
            ans = restore_values(jobs, prev, dp)
            assert restore_parents(jobs, parents) == ans
            env = {"intervals": intervals, "prepare_jobs": module.prepare_jobs}
            expected = (dp[-1] + sum(w for _, w in empty), sorted(ans + [i for i, _ in empty]))
        elif kind == "lis":
            a = [rng.randrange(-3, 5) for _ in range(rng.randrange(10))]
            dp, end = build_values(a)
            val_with_parents, end_with_parents, parents = optimize(a)
            assert (val_with_parents, end_with_parents) == (max(dp, default=0), end)
            for ans in (restore_values(a, dp, end), restore_parents(end, parents)):
                assert all(i < j and a[i] < a[j] for i, j in pairwise(ans))
                assert len(ans) == max(dp, default=0)
            env = {"a": a}
            expected = max(dp, default=0), None
        else:
            p = [rng.randrange(1, 6) for _ in range(rng.randrange(2, 8))]
            dp = build_values(p)
            val_with_parents, parents = optimize(p)
            assert val_with_parents == dp[0][-1]
            ans = restore_values(p, dp)
            assert restore_parents(p, parents) == ans
            env = {"p": p}
            expected = dp[0][-1], ans
        for code, variant in zip(snippets, (module, module), strict=True):
            scope = vars(variant).copy() | env
            exec(code, scope)  # noqa: S102 - execute the repository lesson snippets
            assert scope["val"] == expected[0]
            if kind == "lis":
                assert len(scope["ans"]) == expected[0]
                assert all(x < y for x, y in pairwise(scope["ans"]))
            else:
                assert scope["ans"] == expected[1]
