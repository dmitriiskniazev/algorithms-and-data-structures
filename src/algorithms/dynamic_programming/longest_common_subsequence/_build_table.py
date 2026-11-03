def build_table(first: str, second: str) -> list[list[int]]:
    m, n = len(first), len(second)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        first_char = first[i - 1]
        for j in range(1, n + 1):
            second_char = second[j - 1]
            if first_char == second_char:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp
