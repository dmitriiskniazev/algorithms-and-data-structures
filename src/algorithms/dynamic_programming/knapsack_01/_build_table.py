from collections.abc import Sequence


def build_table(weights: Sequence[int], values: Sequence[int], capacity: int) -> list[list[int]]:
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight, value = weights[i - 1], values[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if weight <= c:
                candidate = dp[i - 1][c - weight] + value
                dp[i][c] = max(dp[i][c], candidate)
    return dp
