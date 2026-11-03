import pytest

from algorithms.dynamic_programming import fibonacci

VERSIONS = [fibonacci.recursive, fibonacci.memoized, fibonacci.tabulated, fibonacci.constant_space]


@pytest.mark.parametrize("implementation", VERSIONS)
def test_known_sequence(implementation):
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    assert [implementation(n) for n in range(len(expected))] == expected


def test_large_exact_value_and_independent_memoized_calls():
    expected = int(
        "4346655768693745643568852767504062580256466051737178040248172908953655541794"
        "9051890403879840079255169295922593080322634775209689623239873322471161642996"
        "440906533187938298969649928516003704476137795166849228875"
    )
    assert fibonacci.constant_space(1000) == fibonacci.tabulated(1000) == expected
    assert fibonacci.memoized(30) == 832040
    assert fibonacci.memoized(0) == 0
    assert fibonacci.memoized(20) == 6765


def test_cassini_identity():
    for n in range(1, 100):
        assert (
            fibonacci.constant_space(n + 1) * fibonacci.constant_space(n - 1) - fibonacci.constant_space(n) ** 2
            == (-1) ** n
        )
