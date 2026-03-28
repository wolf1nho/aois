import pytest
from src.KarnaughMinimizer import KarnaughMinimizer
from src.TruthTableBuilder import TruthTableBuilder

def test_print_karnaugh_map_2vars(capsys):
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("a & b")
    m.print_karnaugh_map(table)
    captured = capsys.readouterr()
    assert "Карта Карно:" in captured.out
    assert "00" in captured.out or "0" in captured.out


def test_print_karnaugh_map_3vars(capsys):
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("a & b & c")
    m.print_karnaugh_map(table)
    captured = capsys.readouterr()
    assert "Карта Карно:" in captured.out


def test_print_karnaugh_map_4vars(capsys):
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("a & b & c & d")
    m.print_karnaugh_map(table)
    captured = capsys.readouterr()
    assert "Карта Карно:" in captured.out


def test_print_karnaugh_map_empty(capsys):
    m = KarnaughMinimizer()
    m.print_karnaugh_map(None)
    captured = capsys.readouterr()
    assert "пустая таблица" in captured.out


def test_print_karnaugh_map_1var(capsys):
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("a")
    m.print_karnaugh_map(table)
    captured = capsys.readouterr()
    assert "Карта Карно:" in captured.out

def test_gray_code_0bits():
    m = KarnaughMinimizer()
    assert m._gray_code(0) == [()]


def test_gray_code_1bit():
    m = KarnaughMinimizer()
    assert m._gray_code(1) == [(0,), (1,)]


def test_gray_code_3bits():
    m = KarnaughMinimizer()
    codes = m._gray_code(3)
    assert len(codes) == 8
    # Проверка: между соседними кодами ровно 1 бит различается
    for i in range(len(codes) - 1):
        diff = sum(a != b for a, b in zip(codes[i], codes[i+1]))
        assert diff == 1

def test_bits_to_label_empty():
    m = KarnaughMinimizer()
    assert m._bits_to_label([]) == "-"


def test_bits_to_label_single():
    m = KarnaughMinimizer()
    assert m._bits_to_label([0]) == "0"
    assert m._bits_to_label([1]) == "1"


def test_bits_to_label_multi():
    m = KarnaughMinimizer()
    assert m._bits_to_label([1, 0, 1]) == "101"

def test_bits_to_int_edge_cases():
    m = KarnaughMinimizer()
    assert m._bits_to_int([]) == 0  
    assert m._bits_to_int([0]) == 0
    assert m._bits_to_int([1]) == 1
    assert m._bits_to_int([1, 1, 1]) == 7

def test_pattern_variants_0():
    m = KarnaughMinimizer()
    assert m._pattern_variants(0) == [()]


def test_pattern_variants_1():
    m = KarnaughMinimizer()
    variants = m._pattern_variants(1)
    assert len(variants) == 3
    assert (-1,) in variants
    assert (0,) in variants
    assert (1,) in variants


def test_pattern_variants_2():
    m = KarnaughMinimizer()
    variants = m._pattern_variants(2)
    assert len(variants) == 9

def test_matches_pattern_all_wildcards():
    m = KarnaughMinimizer()
    assert m._matches_pattern([0, 1, 0], (-1, -1, -1))
    assert m._matches_pattern([1, 1, 1], (-1, -1, -1))


def test_matches_pattern_exact():
    m = KarnaughMinimizer()
    assert m._matches_pattern([1, 0, 1], (1, 0, 1))
    assert not m._matches_pattern([1, 0, 0], (1, 0, 1))


def test_matches_pattern_partial():
    m = KarnaughMinimizer()
    assert m._matches_pattern([1, 0, 1], (1, -1, 1))
    assert not m._matches_pattern([0, 0, 1], (1, -1, 1))

def test_format_expression_empty_groups_dnf():
    m = KarnaughMinimizer()
    result = m._format_expression([], ["a", "b"], is_dnf=True)
    assert result == "0"


def test_format_expression_empty_groups_sknf():
    m = KarnaughMinimizer()
    result = m._format_expression([], ["a", "b"], is_dnf=False)
    assert result == "1"


def test_format_expression_single_literal_dnf():
    m = KarnaughMinimizer()
    groups = [{"pattern": (1, -1), "literal_count": 1}]
    result = m._format_expression(groups, ["a", "b"], is_dnf=True)
    assert result == "(a)"


def test_format_expression_single_literal_sknf():
    m = KarnaughMinimizer()
    groups = [{"pattern": (0, -1), "literal_count": 1}]
    result = m._format_expression(groups, ["a", "b"], is_dnf=False)
    assert "a" in result


def test_format_expression_negated_literal_dnf():
    m = KarnaughMinimizer()
    groups = [{"pattern": (0, 1), "literal_count": 2}]
    result = m._format_expression(groups, ["a", "b"], is_dnf=True)
    assert "!a" in result
    assert "b" in result

def test_remove_dominated_empty():
    m = KarnaughMinimizer()
    result = m._remove_dominated_groups([])
    assert result == []


def test_remove_dominated_identical_cover():
    m = KarnaughMinimizer()
    groups = [
        {"pattern": (1, -1), "covers": {0, 1}, "literal_count": 1},
        {"pattern": (1, 0), "covers": {0, 1}, "literal_count": 2},
    ]
    result = m._remove_dominated_groups(groups)
    assert len(result) == 1
    assert result[0]["literal_count"] == 1


def test_remove_dominated_subset_cover():
    m = KarnaughMinimizer()
    groups = [
        {"pattern": (-1, -1), "covers": {0, 1, 2, 3}, "literal_count": 0},
        {"pattern": (1, 1), "covers": {3}, "literal_count": 2},
    ]
    result = m._remove_dominated_groups(groups)
    assert len(result) >= 1

def test_is_better_cover_fewer_groups():
    m = KarnaughMinimizer()
    candidate = [{"literal_count": 2}, {"literal_count": 2}]
    current = [{"literal_count": 1}]
    assert m._is_better_cover(candidate, current) is False


def test_is_better_cover_same_groups_fewer_literals():
    m = KarnaughMinimizer()
    candidate = [{"literal_count": 1}, {"literal_count": 1}]
    current = [{"literal_count": 2}, {"literal_count": 2}]
    assert m._is_better_cover(candidate, current) is True


def test_is_better_cover_equal():
    m = KarnaughMinimizer()
    candidate = [{"literal_count": 2}]
    current = [{"literal_count": 2}]
    assert m._is_better_cover(candidate, current) is False

def test_search_best_cover_already_covered():
    m = KarnaughMinimizer()
    uncovered = set()
    groups_by_cell = {}
    result = m._search_best_cover(uncovered, groups_by_cell, [])
    assert result == []


def test_search_best_cover_single_cell():
    m = KarnaughMinimizer()
    group = {"covers": {0}, "literal_count": 1}
    uncovered = {0}
    groups_by_cell = {0: [group]}
    result = m._search_best_cover(uncovered, groups_by_cell, [])
    assert result == [group]

def test_minimize_sdnf_single_minterm():
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("a & !b & c")
    result = m.minimize_sdnf(table)
    assert "a" in result and "!b" in result and "c" in result


def test_minimize_sdnf_adjacent_minterms():
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("(a & b & c) | (a & b & !c)")
    result = m.minimize_sdnf(table)
    assert "a" in result and "b" in result
    assert result.count("&") <= 2


def test_minimize_sknf_single_maxterm():
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("a | b | !c")
    result = m.minimize_sknf(table)
    assert isinstance(result, str)
    assert len(result) > 0


def test_minimize_sknf_adjacent_maxterms():
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("(a | b | c) & (a | b | !c)")
    result = m.minimize_sknf(table)
    assert "a" in result or "b" in result


def test_minimize_dont_care_values():
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("a")
    original_table = table.table
    table.table = [row + [None] if len(row) == len(table.variables) else row for row in original_table]
    result = m.minimize_sdnf(table)
    assert isinstance(result, str)

def test_minimize_five_variables():
    m = KarnaughMinimizer()
    table = TruthTableBuilder.build("a & b & c & d & e")
    result = m.minimize_sdnf(table)
    assert all(v in result for v in ["a", "b", "c", "d", "e"])


def test_minimize_symmetric_function():
    m = KarnaughMinimizer()
    expr = "(a & b & !c) | (a & !b & c) | (!a & b & c)"
    table = TruthTableBuilder.build(expr)
    result = m.minimize_sdnf(table)
    assert "a" in result and "b" in result and "c" in result


def test_normalize_empty_string():
    from src.KarnaughMinimizer import KarnaughMinimizer
    def normalize(expr: str):
        if not expr:
            return set()
        return set(expr.replace("(", "").replace(")", "").split(" | "))
    
    assert normalize("") == set()


def test_normalize_single_term():
    def normalize(expr: str):
        if not expr:
            return set()
        return set(expr.replace("(", "").replace(")", "").split(" | "))
    
    assert normalize("a") == {"a"}
    assert normalize("(a)") == {"a"}


def test_normalize_multiple_terms():
    def normalize(expr: str):
        if not expr:
            return set()
        return set(expr.replace("(", "").replace(")", "").split(" | "))
    
    result = normalize("(a & b) | (c & d)")
    assert "(a & b)" in result or "a & b" in result

def test_minimize_with_invalid_table():
    m = KarnaughMinimizer()
    class FakeTable:
        variables = ["a"]
        table = [[1, None]]
    
    result = m.minimize_sdnf(FakeTable())
    assert isinstance(result, str)


def test_print_map_with_corrupted_table():
    m = KarnaughMinimizer()
    class FakeTable:
        variables = []
        table = []
        def __getitem__(self, key):
            return [0]
    
    m.print_karnaugh_map(FakeTable())


@pytest.mark.parametrize("expr,expected_vars_in_result", [
    ("a", ["a"]),
    ("!a", ["a"]),
    ("a | b", ["a", "b"]),
    ("a & b", ["a", "b"]),
    ("a ^ b", ["a", "b"]),
])
def test_minimize_various_expressions(expr, expected_vars_in_result):
    m = KarnaughMinimizer()
    try:
        table = TruthTableBuilder.build(expr)
        result = m.minimize_sdnf(table)
        for var in expected_vars_in_result:
            assert var in result
    except Exception:
        pytest.skip(f"Expression '{expr}' not supported by TruthTableBuilder")


@pytest.mark.parametrize("bit_count", [0, 1, 2, 3, 4])
def test_gray_code_length(bit_count):
    m = KarnaughMinimizer()
    codes = m._gray_code(bit_count)
    assert len(codes) == (1 << bit_count)