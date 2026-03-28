import pytest
from src.Validator import Validator


def test_valid_simple():
    v = Validator()
    assert v.validate_expression("a")
    assert v.get_message() == ""


def test_valid_complex():
    v = Validator()
    assert v.validate_expression("!(a & b) | c")


def test_valid_with_implication():
    v = Validator()
    assert v.validate_expression("(a -> b)")


def test_empty_expression():
    v = Validator()
    assert not v.validate_expression("")
    assert v.get_message() == "Выражение пустое"


def test_invalid_characters():
    v = Validator()
    assert not v.validate_expression("a + b")
    assert v.get_message() == "Недопустимые символы в выражении"


def test_unbalanced_parentheses_left():
    v = Validator()
    assert not v.validate_expression("(a & b")
    assert v.get_message() == "Несбалансированные скобки"


def test_unbalanced_parentheses_right():
    v = Validator()
    assert not v.validate_expression("a & b)")
    assert v.get_message() == "Несбалансированные скобки"


def test_too_many_variables():
    v = Validator()
    assert not v.validate_expression("a & b & c & d & e & f")
    assert v.get_message() == "Слишком много переменных (максимум 5)"


def test_multiple_binary_ops_without_parentheses():
    v = Validator()
    assert not v.validate_expression("a & b | c")
    assert v.get_message() == "Необходимо использовать скобки для связки операций"


def test_unexpected_close_parenthesis():
    v = Validator()
    assert not v.validate_expression("(a & )")
    assert v.get_message() == "Неожиданная )"


def test_unexpected_binary_operator():
    v = Validator()
    assert not v.validate_expression("& a")
    assert v.get_message() == "Неожиданный бинарный оператор"


def test_not_after_operand():
    v = Validator()
    assert not v.validate_expression("a !")
    assert v.get_message() == "! после операнда"


def test_expression_ends_with_operator():
    v = Validator()
    assert not v.validate_expression("a &")
    assert v.get_message() == "Выражение заканчивается оператором"


def test_double_negation_valid():
    v = Validator()
    assert v.validate_expression("!!a")


def test_nested_parentheses_valid():
    v = Validator()
    assert v.validate_expression("((a))")


def test_equivalence_operator():
    v = Validator()
    assert v.validate_expression("(a ~ b)")


def test_long_valid_expression():
    v = Validator()
    assert v.validate_expression("!(a & (b | c)) -> d")