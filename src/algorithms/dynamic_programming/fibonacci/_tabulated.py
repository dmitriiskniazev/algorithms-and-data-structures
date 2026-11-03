def tabulated(n: int) -> int:
    if n < 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for k in range(2, n + 1):
        dp[k] = dp[k - 1] + dp[k - 2]
    return dp[n]
