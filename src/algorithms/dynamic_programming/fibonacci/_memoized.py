def memoized(n: int) -> int:
    memo = {0: 0, 1: 1}
    return _solve(n, memo)


def _solve(n: int, memo: dict[int, int]) -> int:
    if n not in memo:
        memo[n] = _solve(n - 1, memo) + _solve(n - 2, memo)
    return memo[n]
