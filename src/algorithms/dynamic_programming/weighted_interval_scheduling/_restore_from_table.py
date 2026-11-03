from collections.abc import Sequence

from algorithms.dynamic_programming.weighted_interval_scheduling._types import Job


def restore_from_table(jobs: Sequence[Job], prev: Sequence[int], dp: Sequence[int]) -> list[int]:
    ans: list[int] = []
    j = len(jobs)
    while j > 0:
        if dp[j] == dp[j - 1]:
            j -= 1
        else:
            ans.append(jobs[j - 1].index)
            j = prev[j - 1]
    return ans
