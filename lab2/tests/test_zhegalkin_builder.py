import pytest
from src.ZhegalkinBuilder import ZhegalkinBuilder
from src.TruthTableBuilder import TruthTableBuilder


def test_constant_zero():
    table = TruthTableBuilder.build("a & !a")  # всегда 0
    z = ZhegalkinBuilder()
    z.build(table)

    assert z.polynomial == []
    assert z.is_linear()


def test_constant_one():
    table = TruthTableBuilder.build("a | !a")  # всегда 1
    z = ZhegalkinBuilder()
    z.build(table)

    assert z.polynomial == ["1"]
    assert z.is_linear()


def test_identity_function():
    table = TruthTableBuilder.build("a")
    z = ZhegalkinBuilder()
    z.build(table)

    assert z.polynomial == ["a"]
    assert z.is_linear()


def test_not_function():
    table = TruthTableBuilder.build("!a")
    z = ZhegalkinBuilder()
    z.build(table)

    assert set(z.polynomial) == {"1", "a"}
    assert z.is_linear()


def test_and_function():
    table = TruthTableBuilder.build("a & b")
    z = ZhegalkinBuilder()
    z.build(table)

    assert z.polynomial == ["ab"]
    assert not z.is_linear()


def test_or_function():
    table = TruthTableBuilder.build("a | b")
    z = ZhegalkinBuilder()
    z.build(table)

    assert set(z.polynomial) == {"a", "b", "ab"}
    assert not z.is_linear()


def test_xor_equivalence():
    table = TruthTableBuilder.build("a ~ b")
    z = ZhegalkinBuilder()
    z.build(table)

    assert set(z.polynomial) == {"1", "a", "b"}
    assert z.is_linear()


def test_xor_manual():
    table = TruthTableBuilder.build("(a | b) & !(a & b)")
    z = ZhegalkinBuilder()
    z.build(table)

    assert set(z.polynomial) == {"a", "b"}
    assert z.is_linear()


def test_three_variables():
    table = TruthTableBuilder.build("a & b & c")
    z = ZhegalkinBuilder()
    z.build(table)

    assert z.polynomial == ["abc"]
    assert not z.is_linear()


def test_mixed_expression():
    table = TruthTableBuilder.build("!(a & b) | c")
    z = ZhegalkinBuilder()
    z.build(table)

    assert isinstance(z.polynomial, list)
    assert all(isinstance(x, str) for x in z.polynomial)


def test_polynomial_order_independent():
    table = TruthTableBuilder.build("b & a")
    z = ZhegalkinBuilder()
    z.build(table)

    assert z.polynomial == ["ab"]