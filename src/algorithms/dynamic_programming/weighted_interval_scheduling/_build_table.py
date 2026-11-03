from bisect import bisect_right
from collections.abc import Sequence

from algorithms.dynamic_programming.weighted_interval_scheduling._types import Job


def build_table(jobs: Sequence[Job]) -> tuple[list[int], list[int]]:
    n = len(jobs)
    finishes = [job.finish for job in jobs]
    prev = [bisect_right(finishes, jobs[j].start, 0, j) for j in range(n)]
    dp = [0] * (n + 1)
    for j, job in enumerate(jobs):
        dp[j + 1] = max(dp[j], dp[prev[j]] + job.weight)
    return dp, prev
