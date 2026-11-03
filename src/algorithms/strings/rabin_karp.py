_MODULUS = 1_000_000_007
_BASE = 911_382_323


def search(text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    power = pow(_BASE, m - 1, _MODULUS)
    pattern_hash = text_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * _BASE + ord(pattern[i]) + 1) % _MODULUS
        text_hash = (text_hash * _BASE + ord(text[i]) + 1) % _MODULUS

    matches: list[int] = []
    for i in range(n - m + 1):
        if text_hash == pattern_hash and text.startswith(pattern, i):
            matches.append(i)
        if i < n - m:
            outgoing = (ord(text[i]) + 1) * power
            text_hash = ((text_hash - outgoing) * _BASE + ord(text[i + m]) + 1) % _MODULUS
    return matches
