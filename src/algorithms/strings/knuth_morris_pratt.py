from algorithms.strings.prefix_function import compute


def search(text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    pi = compute(pattern)
    matches: list[int] = []
    j = 0
    for i, symbol in enumerate(text):
        while j and symbol != pattern[j]:
            j = pi[j - 1]
        if symbol == pattern[j]:
            j += 1
        if j == m:
            matches.append(i - m + 1)
            j = pi[j - 1]
    return matches
