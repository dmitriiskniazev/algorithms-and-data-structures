from collections.abc import Sequence

from algorithms.dynamic_programming.weighted_interval_scheduling._types import Job, Step


def restore_from_parents(jobs: Sequence[Job], parent: Sequence[Step]) -> list[int]:
    ans: list[int] = []
    state = len(jobs)
    while state > 0:
        prev, item = parent[state]
        if item is not None:
            ans.append(item)
        state = prev
    return ans
