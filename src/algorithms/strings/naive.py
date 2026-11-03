def search(text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    return [i for i in range(n - m + 1) if text.startswith(pattern, i)]
