from algorithms.strings.z_function import compute


def search(text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    combined: list[str | None] = [*pattern, None, *text]
    # None is distinct from every character in either input.
    z = compute(combined)
    return [i for i in range(n - m + 1) if z[m + 1 + i] >= m]
