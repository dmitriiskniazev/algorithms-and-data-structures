from collections.abc import Iterable


def select(intervals: Iterable[tuple[int, int]]) -> list[int]:
    indexed = list(enumerate(intervals))
    for _, (start, finish) in indexed:
        if start > finish:
            raise ValueError("interval start must not exceed finish")

    indexed.sort(key=lambda item: (item[1][1], item[0]))
    ans: list[int] = []
    last_finish: int | None = None
    for i, (start, finish) in indexed:
        if last_finish is None or start >= last_finish:
            ans.append(i)
            last_finish = finish
    return ans
