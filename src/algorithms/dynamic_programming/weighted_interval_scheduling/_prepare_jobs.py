from collections.abc import Sequence

from algorithms.dynamic_programming.weighted_interval_scheduling._types import Job


def prepare_jobs(intervals: Sequence[tuple[int, int, int]]) -> tuple[list[Job], list[tuple[int, int]]]:
    jobs: list[Job] = []
    empty: list[tuple[int, int]] = []
    for i, (start, finish, weight) in enumerate(intervals):
        if any(not isinstance(item, int) or isinstance(item, bool) for item in (start, finish, weight)):
            raise ValueError("interval coordinates and weights must be integers")
        if start > finish:
            raise ValueError("interval start must not exceed finish")
        if start == finish:
            if weight > 0:
                empty.append((i, weight))
        else:
            jobs.append(Job(finish, start, i, weight))
    jobs.sort(key=lambda job: (job.finish, job.start, job.index))
    return jobs, empty
