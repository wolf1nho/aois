import pytest
from src.CanonicalFormsBuilder import CanonicalFormsBuilder
from src.TruthTableBuilder import TruthTableBuilder



def test_sdnf_simple_and():
    table = TruthTableBuilder.build("a & b")
    c = CanonicalFormsBuilder()

    sdnf = c.build_sdnf(table)

    assert sdnf == "(a & b)"


def test_sknf_simple_and():
    table = TruthTableBuilder.build("a & b")
    c = CanonicalFormsBuilder()

    sknf = c.build_sknf(table)

    assert sknf == "(a | b) & (a | !b) & (!a | b)"


def test_sdnf_or():
    table = TruthTableBuilder.build("a | b")
    c = CanonicalFormsBuilder()

    sdnf = c.build_sdnf(table)

    expected = {
        "(!a & b) | (a & !b) | (a & b)",
        "(a & !b) | (!a & b) | (a & b)",
        "(a & b) | (!a & b) | (a & !b)"
    }

    assert sdnf in expected


def test_sknf_or():
    table = TruthTableBuilder.build("a | b")
    c = CanonicalFormsBuilder()

    sknf = c.build_sknf(table)

    assert sknf == "(a | b)"


def test_constant_zero():
    table = TruthTableBuilder.build("a & !a")
    c = CanonicalFormsBuilder()

    assert c.build_sdnf(table) == "0"
    assert c.build_sknf(table) != ""


def test_constant_one():
    table = TruthTableBuilder.build("a | !a")
    c = CanonicalFormsBuilder()

    assert c.build_sdnf(table) != ""
    assert c.build_sknf(table) == "1"


def test_numeric_forms_and():
    table = TruthTableBuilder.build("a & b")
    c = CanonicalFormsBuilder()

    c.to_numeric_form(table)

    assert c.get_num_sdnf() == [3]
    assert set(c.get_num_sknf()) == {0, 1, 2}


def test_numeric_forms_or():
    table = TruthTableBuilder.build("a | b")
    c = CanonicalFormsBuilder()

    c.to_numeric_form(table)

    assert set(c.get_num_sdnf()) == {1, 2, 3}
    assert c.get_num_sknf() == [0]


def test_bin_to_int():
    c = CanonicalFormsBuilder()

    assert c._bin_to_int([0, 0]) == 0
    assert c._bin_to_int([0, 1]) == 1
    assert c._bin_to_int([1, 0]) == 2
    assert c._bin_to_int([1, 1]) == 3


def test_index_form_and():
    table = TruthTableBuilder.build("a & b")
    c = CanonicalFormsBuilder()

    index = c.get_index_form(table)

    assert index == 1


def test_index_form_or():
    table = TruthTableBuilder.build("a | b")
    c = CanonicalFormsBuilder()

    index = c.get_index_form(table)

    assert index == 7


def test_three_variables_sdnf():
    table = TruthTableBuilder.build("a & b & c")
    c = CanonicalFormsBuilder()

    sdnf = c.build_sdnf(table)

    assert sdnf == "(a & b & c)"


def test_three_variables_numeric():
    table = TruthTableBuilder.build("a & b & c")
    c = CanonicalFormsBuilder()

    c.to_numeric_form(table)

    assert c.get_num_sdnf() == [7]