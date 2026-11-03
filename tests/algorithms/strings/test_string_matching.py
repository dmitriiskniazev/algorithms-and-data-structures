from algorithms.strings import knuth_morris_pratt, naive, prefix_function, rabin_karp, z_function, z_search


def test_searches_return_all_overlapping_matches() -> None:
    for search in (naive.search, knuth_morris_pratt.search, z_search.search, rabin_karp.search):
        assert search("ababa", "aba") == [0, 2]
        assert search("aaaaa", "aaa") == [0, 1, 2]


def test_empty_and_too_long_patterns() -> None:
    for search in (naive.search, knuth_morris_pratt.search, z_search.search, rabin_karp.search):
        assert search("abc", "") == [0, 1, 2, 3]
        assert search("", "a") == []
        assert search("a", "aa") == []


def test_prefix_and_z_values() -> None:
    assert prefix_function.compute("ababaca") == [0, 0, 1, 2, 3, 0, 1]
    assert z_function.compute("ababaca") == [7, 0, 3, 0, 1, 0, 1]
    assert z_function.compute("") == []


def test_z_search_separator_cannot_collide_with_input() -> None:
    text = "\0🙂\0🙂\0"
    pattern = "\0🙂"
    assert z_search.search(text, pattern) == [0, 2]


def test_rabin_karp_verifies_a_real_hash_collision() -> None:
    # These distinct four-symbol sequences collide for the implementation's fixed parameters.
    text = "".join(map(chr, (0xCF, 0x2F, 0x27, 0x38)))
    pattern = "".join(map(chr, (0xC5, 0xA1, 0x58, 0x86)))
    assert rabin_karp.search(text, pattern) == []


def test_all_searches_match_brute_force_on_small_alphabet() -> None:
    words = [""]
    for _ in range(4):
        words += [word + symbol for word in tuple(words) for symbol in "ab"]
    for text in words:
        for pattern in words:
            expected = [index for index in range(len(text) - len(pattern) + 1) if text.startswith(pattern, index)]
            for search in (naive.search, knuth_morris_pratt.search, z_search.search, rabin_karp.search):
                assert search(text, pattern) == expected
