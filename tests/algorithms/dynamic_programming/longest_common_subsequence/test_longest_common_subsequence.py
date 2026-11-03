from algorithms.dynamic_programming import longest_common_subsequence


def is_subsequence(candidate: str, text: str) -> bool:
    position = 0
    for char in text:
        if position < len(candidate) and candidate[position] == char:
            position += 1
    return position == len(candidate)


def test_lcs_is_common_and_has_known_optimal_length() -> None:
    result = longest_common_subsequence.solve("ABCBDAB", "BDCABA")
    assert is_subsequence(result, "ABCBDAB")
    assert is_subsequence(result, "BDCABA")
    assert len(result) == 4


def test_lcs_empty_and_identical_inputs() -> None:
    assert longest_common_subsequence.solve("", "abc") == ""
    assert longest_common_subsequence.solve("same", "same") == "same"
