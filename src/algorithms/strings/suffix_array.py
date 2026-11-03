def build(text: str) -> tuple[list[int], list[int]]:
    n = len(text)
    order = list(range(n))
    if n <= 1:
        return order, [0] * n
    rank = [ord(symbol) for symbol in text]
    width = 1
    while width < n:
        order.sort(key=lambda i: (rank[i], rank[i + width] if i + width < n else -1))
        next_rank = [0] * n
        for k in range(1, n):
            prev, curr = order[k - 1], order[k]
            prev_pair = (rank[prev], rank[prev + width] if prev + width < n else -1)
            curr_pair = (rank[curr], rank[curr + width] if curr + width < n else -1)
            next_rank[curr] = next_rank[prev] + (curr_pair != prev_pair)
        rank = next_rank
        if rank[order[-1]] == n - 1:
            break
        width *= 2

    lcp = [0] * n
    h = 0
    for i in range(n):
        k = rank[i]
        if k == 0:
            continue
        prev = order[k - 1]
        while i + h < n and prev + h < n and text[i + h] == text[prev + h]:
            h += 1
        lcp[k] = h
        h = max(h - 1, 0)
    return order, lcp
