import pytest
from CalculationMinimizer import CalculationMinimizer
from src.CalculationTabularMinimizer import CalculationTabularMinimizer
from src.TruthTableBuilder import TruthTableBuilder

def normalize(expr: str):
    return set(expr.replace("(", "").replace(")", "").split(" | "))


def test_constant_zero():
    table = TruthTableBuilder.build("a & !a")
    m = CalculationTabularMinimizer()

    result = m.minimize_sdnf(table)

    assert result == "0"


def test_constant_one():
    table = TruthTableBuilder.build("a | !a")
    m = CalculationTabularMinimizer()

    result = m.minimize_sknf(table)

    assert result == "1"

def test_simple_and():
    table = TruthTableBuilder.build("a & b")
    m = CalculationTabularMinimizer()

    result = m.minimize_sdnf(table)

    assert "a" in result and "b" in result

def test_simple_or():
    table = TruthTableBuilder.build("a | b")
    m = CalculationTabularMinimizer()

    result = m.minimize_sdnf(table)

    terms = normalize(result)
    assert terms == {"a", "b"} or len(terms) <= 2


def test_xor_not_simplified():
    table = TruthTableBuilder.build("(a | b) & !(a & b)")
    m = CalculationTabularMinimizer()

    result = m.minimize_sdnf(table)

    assert "|" in result


def test_redundant_variable():
    table = TruthTableBuilder.build("a & (b | !b)")
    m = CalculationTabularMinimizer()

    result = m.minimize_sdnf(table)

    assert result.strip("()") == "a"


def test_three_variables():
    table = TruthTableBuilder.build("a & b & c")
    m = CalculationTabularMinimizer()

    result = m.minimize_sdnf(table)

    assert all(v in result for v in ["a", "b", "c"])


def test_sknf_simple():
    table = TruthTableBuilder.build("a & b")
    m = CalculationTabularMinimizer()

    result = m.minimize_sknf(table)

    assert "&" in result or "|" in result


def test_sknf_constant_one():
    table = TruthTableBuilder.build("a | !a")
    m = CalculationTabularMinimizer()

    result = m.minimize_sknf(table)

    assert result == "1"


def test_sknf_constant_zero():
    table = TruthTableBuilder.build("a & !a")
    m = CalculationTabularMinimizer()

    result = m.minimize_sknf(table)

    assert result != ""


def test_getters():
    table = TruthTableBuilder.build("a & b")
    m = CalculationTabularMinimizer()

    m.minimize_sdnf(table)
    m.minimize_sknf(table)

    assert isinstance(m.get_minimized_sdnf(), str)
    assert isinstance(m.get_minimized_sknf(), str)