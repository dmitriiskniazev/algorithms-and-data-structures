from collections.abc import Sequence

from algorithms.dynamic_programming.weighted_interval_scheduling._build_table import build_table
from algorithms.dynamic_programming.weighted_interval_scheduling._prepare_jobs import prepare_jobs
from algorithms.dynamic_programming.weighted_interval_scheduling._restore_from_table import restore_from_table


def solve(intervals: Sequence[tuple[int, int, int]]) -> tuple[int, list[int]]:
    jobs, empty = prepare_jobs(intervals)
    dp, prev = build_table(jobs)
    ans = restore_from_table(jobs, prev, dp)
    ans.extend(i for i, _ in empty)
    ans.sort()
    return dp[-1] + sum(weight for _, weight in empty), ans
