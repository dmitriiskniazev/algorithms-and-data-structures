def constant_space(n: int) -> int:
    prev, curr = 1, 0
    for _ in range(n):
        prev, curr = curr, prev + curr
    return curr
