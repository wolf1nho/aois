import pytest
from src.PostAnalyser import PostAnalyser
from src.TruthTableBuilder import TruthTableBuilder


def test_t0_property():
    table = TruthTableBuilder.build("a & b")
    p = PostAnalyser()
    p.execute(table)

    assert p.t0 is True


def test_not_t0():
    table = TruthTableBuilder.build("a | b")
    p = PostAnalyser()
    p.execute(table)

    assert p.t0 is True


def test_t1_property():
    table = TruthTableBuilder.build("a | b")
    p = PostAnalyser()
    p.execute(table)

    assert p.t1 is True


def test_not_t1():
    table = TruthTableBuilder.build("a & b")
    p = PostAnalyser()
    p.execute(table)

    assert p.t1 is True


def test_self_dual_true():
    table = TruthTableBuilder.build("a")
    p = PostAnalyser()
    p.execute(table)

    assert p.s is True


def test_self_dual_false():
    table = TruthTableBuilder.build("a & b")
    p = PostAnalyser()
    p.execute(table)

    assert p.s is False


def test_monotone_true_and():
    table = TruthTableBuilder.build("a & b")
    p = PostAnalyser()
    p.execute(table)

    assert p.m is True


def test_monotone_true_or():
    table = TruthTableBuilder.build("a | b")
    p = PostAnalyser()
    p.execute(table)

    assert p.m is True


def test_monotone_false():
    table = TruthTableBuilder.build("!a")
    p = PostAnalyser()
    p.execute(table)

    assert p.m is False


def test_all_properties_constant_zero():
    table = TruthTableBuilder.build("a & !a")
    p = PostAnalyser()
    p.execute(table)

    assert p.t0 is True
    assert p.t1 is False
    assert p.s is False
    assert p.m is True


def test_all_properties_constant_one():
    table = TruthTableBuilder.build("a | !a")
    p = PostAnalyser()
    p.execute(table)

    assert p.t0 is False
    assert p.t1 is True
    assert p.s is False
    assert p.m is True