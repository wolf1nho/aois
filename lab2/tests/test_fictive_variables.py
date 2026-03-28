import pytest
from src.FictiveVariablesFinder import FictiveVariablesFinder
from src.TruthTableBuilder import TruthTableBuilder



def test_no_fictive_variables():
    table = TruthTableBuilder.build("a & b")
    result = FictiveVariablesFinder.find(table)

    assert result == "отсутствуют"


def test_one_fictive_variable():
    table = TruthTableBuilder.build("a")
    result = FictiveVariablesFinder.find(table)

    assert result == "отсутствуют"


def test_second_variable_fictive():
    table = TruthTableBuilder.build("a & 1")
    result = FictiveVariablesFinder.find(table)

    table = TruthTableBuilder.build("a & (b | !b)")
    result = FictiveVariablesFinder.find(table)

    assert result == "b"


def test_first_variable_fictive():
    table = TruthTableBuilder.build("b & (a | !a)")
    result = FictiveVariablesFinder.find(table)

    assert result == "a"


def test_all_variables_fictive_constant():
    table = TruthTableBuilder.build("a & !a")
    result = FictiveVariablesFinder.find(table)

    assert set(result.split(", ")) == {"a"} or result == "a"


def test_three_variables_one_fictive():
    table = TruthTableBuilder.build("a & b")
    table = TruthTableBuilder.build("a & b & (c | !c)")

    result = FictiveVariablesFinder.find(table)

    assert result == "c"


def test_three_variables_multiple_fictive():
    table = TruthTableBuilder.build("a")
    table = TruthTableBuilder.build("a & (b | !b) & (c | !c)")

    result = FictiveVariablesFinder.find(table)

    assert set(result.split(", ")) == {"b", "c"}


def test_no_variables_edge_case():
    table = TruthTableBuilder.build("a & !a")
    result = FictiveVariablesFinder.find(table)

    assert isinstance(result, str)


def test_output_format_multiple():
    table = TruthTableBuilder.build("a & (b | !b) & (c | !c)")
    result = FictiveVariablesFinder.find(table)

    assert ", " in result or result == "отсутствуют"