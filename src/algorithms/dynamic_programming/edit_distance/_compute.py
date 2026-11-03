def compute(source: str, target: str) -> int:
    if len(source) < len(target):
        source, target = target, source
    n = len(target)
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    for i in range(1, len(source) + 1):
        source_char = source[i - 1]
        curr[0] = i
        for j in range(1, n + 1):
            target_char = target[j - 1]
            curr[j] = min(prev[j - 1] + (source_char != target_char), prev[j] + 1, curr[j - 1] + 1)
        prev, curr = curr, prev
    return prev[-1]
