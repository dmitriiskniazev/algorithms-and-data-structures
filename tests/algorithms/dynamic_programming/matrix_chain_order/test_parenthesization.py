import ast

import pytest

from algorithms.dynamic_programming import matrix_chain_order


def evaluate(expression, dimensions):
    def visit(node):
        if isinstance(node, ast.Name):
            assert node.id.startswith("A")
            index = int(node.id[1:]) - 1
            return dimensions[index], dimensions[index + 1], 0, [index]
        assert isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult)
        rows, inner, left_cost, left_indices = visit(node.left)
        other_inner, cols, right_cost, right_indices = visit(node.right)
        assert inner == other_inner
        return (rows, cols, left_cost + right_cost + rows * inner * cols, left_indices + right_indices)

    return visit(ast.parse(expression, mode="eval").body)


@pytest.mark.parametrize(
    "dimensions, optimum", [([2, 3], 0), ([30, 35, 15, 5, 10, 20, 25], 15125), ([2, 2, 2, 2], 16), ([1] * 13, 11)]
)
def test_parenthesization_preserves_order_and_has_optimal_cost(dimensions, optimum):
    table = matrix_chain_order.build_table(dimensions)
    value, transitions = matrix_chain_order.build_parents(dimensions)
    public_value, public_expression = matrix_chain_order.solve(dimensions)
    assert table[0][-1] == value == public_value == optimum
    for expression in (
        matrix_chain_order.restore_from_table(dimensions, table),
        matrix_chain_order.restore_from_parents(dimensions, transitions),
        public_expression,
    ):
        rows, cols, cost, indices = evaluate(expression, dimensions)
        assert (rows, cols) == (dimensions[0], dimensions[-1])
        assert indices == list(range(len(dimensions) - 1))
        assert cost == optimum


def test_deep_parenthesization_does_not_depend_on_recursion_limit():
    n = 1100
    dimensions = [1] * (n + 1)
    table = [[max(0, j - i) for j in range(n)] for i in range(n)]
    splits = [[i] * n for i in range(n)]
    expected = "".join(f"(A{i}*" for i in range(1, n)) + f"A{n}" + ")" * (n - 1)
    assert matrix_chain_order.restore_from_table(dimensions, table) == expected
    assert matrix_chain_order.restore_from_parents(dimensions, splits) == expected
