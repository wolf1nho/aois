import pytest
from src.TruthTableBuilder import TruthTableBuilder


def test_single_variable():
    table = TruthTableBuilder.build("a")
    assert table.variables == ['a']
    assert table.table == [
        [0, 0],
        [1, 1]
    ]


def test_negation():
    table = TruthTableBuilder.build("!a")
    assert table.table == [
        [0, 1],
        [1, 0]
    ]


def test_and_operator():
    table = TruthTableBuilder.build("a & b")
    assert table.variables == ['a', 'b']
    assert table.table == [
        [0, 0, 0],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 1]
    ]


def test_or_operator():
    table = TruthTableBuilder.build("a | b")
    assert table.table == [
        [0, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]


def test_implication():
    table = TruthTableBuilder.build("a -> b")
    assert table.table == [
        [0, 0, 1],
        [0, 1, 1],
        [1, 0, 0],
        [1, 1, 1]
    ]


def test_equivalence():
    table = TruthTableBuilder.build("a ~ b")
    assert table.table == [
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 1]
    ]


def test_complex_expression():
    table = TruthTableBuilder.build("!(a & b) | c")
    assert table.variables == ['a', 'b', 'c']

    expected = [
        ([0, 0, 0], 1),
        ([1, 1, 0], 0),
        ([1, 1, 1], 1),
    ]

    for values, result in expected:
        for row in table.table:
            if row[:-1] == values:
                assert row[-1] == result


def test_parentheses_priority():
    t1 = TruthTableBuilder.build("a & (b | c)")
    t2 = TruthTableBuilder.build("(a & b) | c")

    assert t1.table != t2.table 


def test_variable_order():
    table = TruthTableBuilder.build("b & a")
    assert table.variables == ['a', 'b']
