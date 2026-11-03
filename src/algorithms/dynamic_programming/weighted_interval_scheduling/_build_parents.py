from bisect import bisect_right
from collections.abc import Sequence

from algorithms.dynamic_programming.weighted_interval_scheduling._types import Job, Parents, Step


def build_parents(jobs: Sequence[Job]) -> tuple[int, Parents]:
    n = len(jobs)
    parent: Parents = [(0, None)] * (n + 1)
    finishes = [job.finish for job in jobs]
    dp = [0] * (n + 1)
    for j, job in enumerate(jobs):
        prev = bisect_right(finishes, job.start, 0, j)
        dp[j + 1] = dp[j]
        step: Step = (j, None)
        candidate = dp[prev] + job.weight
        if candidate > dp[j + 1]:
            dp[j + 1] = candidate
            step = (prev, job.index)
        parent[j + 1] = step
    return dp[-1], parent
