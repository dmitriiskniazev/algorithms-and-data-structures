def recursive(n: int) -> int:
    if n < 2:
        return n
    return recursive(n - 1) + recursive(n - 2)
