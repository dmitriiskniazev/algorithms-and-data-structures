def build_table(source: str, target: str) -> list[list[int]]:
    m, n = len(source), len(target)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        dp[i][0] = i
    for j in range(1, n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        source_char = source[i - 1]
        for j in range(1, n + 1):
            target_char = target[j - 1]
            dp[i][j] = min(dp[i - 1][j - 1] + (source_char != target_char), dp[i - 1][j] + 1, dp[i][j - 1] + 1)
    return dp
