def compute(text: str) -> list[int]:
    pi = [0] * len(text)
    j = 0
    for i in range(1, len(text)):
        while j and text[i] != text[j]:
            j = pi[j - 1]
        if text[i] == text[j]:
            j += 1
        pi[i] = j
    return pi
