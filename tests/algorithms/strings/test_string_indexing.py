from itertools import product

from algorithms.strings import suffix_array
from data_structures.trie import Trie


def test_trie_words_prefixes_and_duplicates() -> None:
    trie = Trie()
    assert trie.starts_with("")
    assert not trie.search("")
    for word in ("", "algorithm", "algebra", "all", "algorithm"):
        trie.insert(word)
    assert trie.search("")
    assert trie.search("algorithm")
    assert trie.search("algebra")
    assert not trie.search("alg")
    assert trie.starts_with("alg")
    assert trie.starts_with("all")
    assert not trie.starts_with("alz")


def _naive_suffix_index(text: str) -> tuple[list[int], list[int]]:
    order = sorted(range(len(text)), key=lambda start: text[start:])
    lcp = [0] * len(text)
    for position in range(1, len(order)):
        left, right = order[position - 1], order[position]
        while (
            left + lcp[position] < len(text)
            and right + lcp[position] < len(text)
            and text[left + lcp[position]] == text[right + lcp[position]]
        ):
            lcp[position] += 1
    return order, lcp


def test_suffix_array_differential_exhaustive() -> None:
    for length in range(8):
        for symbols in product("ab", repeat=length):
            text = "".join(symbols)
            assert suffix_array.build(text) == _naive_suffix_index(text)


def test_suffix_array_unicode_code_points_and_edge_cases() -> None:
    for text in ("", "x", "aaaaaa", "abababa", "banana", "é🙂é"):
        assert suffix_array.build(text) == _naive_suffix_index(text)
