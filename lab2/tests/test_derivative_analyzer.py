import pytest
from DerivativeAnalyzer import DerivativeAnalyzer
from src.TruthTableBuilder import TruthTableBuilder

def test_single_variable_derivative():
    table = TruthTableBuilder.build("a")
    d = DerivativeAnalyzer()
    d.analyze(table)

    # d(a)/da = 1
    assert "a" in d.derivatives
    tb = d.derivatives["a"]
    assert all(row[-1] == 1 for row in tb.table)


def test_not_function_derivative():
    table = TruthTableBuilder.build("!a")
    d = DerivativeAnalyzer()
    d.analyze(table)

    # d(!a)/da = 1
    tb = d.derivatives["a"]
    assert all(row[-1] == 1 for row in tb.table)


def test_or_derivative():
    table = TruthTableBuilder.build("a | b")
    d = DerivativeAnalyzer()
    d.analyze(table)

    da = d.derivatives["a"]
    values = [row[-1] for row in da.table]
    assert values == [1, 0]

    db = d.derivatives["b"]
    values = [row[-1] for row in db.table]
    assert values == [1, 0]


def test_derivative_keys():
    table = TruthTableBuilder.build("a & b & c")
    d = DerivativeAnalyzer()
    d.analyze(table)

    assert set(d.derivatives.keys()) >= {"a", "b", "c"}


def test_sdnf_generation():
    table = TruthTableBuilder.build("a & b")
    d = DerivativeAnalyzer()
    d.analyze(table)

    da = d.derivatives["a"]
    sdnf = d._build_sdnf(da)

    assert sdnf in ["(b)", "(b)"]


def test_sknf_generation():
    table = TruthTableBuilder.build("a & b")
    d = DerivativeAnalyzer()
    d.analyze(table)

    da = d.derivatives["a"]
    sknf = d._build_sknf(da)

    assert isinstance(sknf, str)
    assert sknf != ""


def test_constant_function_derivative():
    table = TruthTableBuilder.build("a & !a")  # 0
    d = DerivativeAnalyzer()
    d.analyze(table)

    for tb in d.derivatives.values():
        assert all(row[-1] == 0 for row in tb.table)