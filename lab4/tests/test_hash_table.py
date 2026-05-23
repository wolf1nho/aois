import pytest
from src.HashTable import HashTable

DATA = [
    ("Абаев", "Тимур"),      # h = 1
    ("Бобков", "Андрей"),    # h = 18
    ("Видерт", "Руслан"),    # h = 15
    ("Вяткин", "Игорь"),     # h = 18 (коллизия)
    ("Кожевников", "Олег"),  # h = 18 (коллизия)
]

@pytest.fixture
def table():
    return HashTable()

def test_insert_and_search(table):
    for key, val in DATA:
        table.insert(key, val)
    
    assert table.search("Абаев") == "Тимур"
    assert table.search("Кожевников") == "Олег"
    assert table.search("Вяткин") == "Игорь"

def test_collision_chaining(table):
    table.insert("Кот", "Андрей")
    table.insert("Вяткин", "Игорь")
    
    h_index = table._hash("Кот")
    assert h_index == 18
    assert table.table[h_index].key == "Кот"
    assert table.table[h_index].P0 is not None
    
    next_idx = table.table[h_index].P0
    assert table.table[next_idx].key == "Вяткин"

def test_duplicate_key_error(table):
    table.insert("Абаев", "Тимур")
    with pytest.raises(Exception, match="уже существует"):
        table.insert("Абаев", "Новое значение")

def test_update(table):
    table.insert("Видерт", "Руслан")
    table.update("Видерт", "Новое Имя")
    assert table.search("Видерт") == "Новое Имя"

def test_delete_terminal(table):
    table.insert("Бобков", "Андрей")
    table.insert("Вяткин", "Игорь")
    
    table.delete("Вяткин")
    
    with pytest.raises(Exception, match="не найден"):
        table.search("Вяткин")
    
    assert table.table[18].P0 is None

def test_delete_middle_relink(table):
    table.insert("Бобков", "Андрей")     
    table.insert("Вяткин", "Игорь")     
    table.insert("Кожевников", "Олег")  
    
    table.delete("Вяткин")
    
    assert table.search("Бобков") == "Андрей"
    assert table.search("Кожевников") == "Олег"
    with pytest.raises(Exception, match="не найден"):
        table.search("Вяткин")

def test_load_factor(table):
    assert table.get_load_factor() == 0.0
    table.insert("Абаев", "Тимур")
    table.insert("Бобков", "Андрей")

    assert table.get_load_factor() == pytest.approx(0.1)

def test_overflow(table):
    small_table = HashTable(size=2)
    small_table.insert("Ключ1", "В1")
    small_table.insert("Ключ2", "В2")
    with pytest.raises(Exception, match="переполнена"):
        small_table.insert("Ключ3", "В3")

def test_ru_letter_to_int_cases(table):
    assert table._ru_letter_to_int('а') == 0   # val < 6
    assert table._ru_letter_to_int('ё') == 6   # val == 33
    assert table._ru_letter_to_int('я') == 32  # else (val + 1)

def test_relocation_of_foreign_node(table):
    table.insert("Бобков", "18") 
    table.insert("Вяткин", "19") 
    
    h_target = table._hash("Вяткин")
    target_idx = table.table[h_target].P0
    
    table.insert("Абаев", "Адрес 1")
    table.insert("Кожевников", "Коллизия 18") 
    
    table.insert("Азимов", "Адрес 8")
    assert table.search("Азимов") == "Адрес 8"

def test_insert_duplicate_raises(table):
    table.insert("Бобков", "1")
    table.insert("Вяткин", "2")
    with pytest.raises(Exception, match="уже существует"):
        table.insert("Вяткин", "3")

def test_update_missing_key_raises(table):
    with pytest.raises(Exception, match="Ключ не найден"):
        table.update("Призрак", "Данные")

def test_delete_middle_complex(table):
    table.insert("Бобков", "1")
    table.insert("Вяткин", "2")
    table.insert("Кожевников", "3")
    
    table.delete("Вяткин")
    assert table.search("Кожевников") == "3"
    assert table.search("Бобков") == "1"

def test_delete_missing_key_raises(table):
    with pytest.raises(Exception, match="не найден"):
        table.delete("Никто")

def test_clear_and_load_factor(table):
    table.insert("Aвраам", "Линкольн")
    table.insert("Джон", "Кеннеди")
    assert table.get_load_factor() == 2/20
    table.clear()
    assert table.get_load_factor() == 0
    with pytest.raises(Exception):
        table.search("A")

def test_table_overflow_exception(table):
    mini_table = HashTable(size=1)
    mini_table.insert("аа", "V1")
    with pytest.raises(Exception, match="Хеш-таблица переполнена"):
        mini_table.insert("аб", "V2")

def test_find_previous_in_chain_none(table):
    """Покрытие строки 112 и 121 (Случаи, когда предыдущего нет)."""
    table.insert("Абаев", "1")
    assert table._find_previous_in_chain(1) is None

def test_insert_and_search(ht):
    ht.insert("аб", 1)
    assert ht.search("аб") == 1


def test_update(ht):
    ht.insert("аб", 1)
    ht.update("аб", 42)
    assert ht.search("аб") == 42


def test_delete(ht):
    ht.insert("аб", 1)
    ht.delete("аб")
    with pytest.raises(Exception):
        ht.search("аб")


@pytest.fixture
def ht():
    return HashTable(size=10)

def test_collision_chain(ht):
    keys = ["аб", "ав", "аг"]

    for i, key in enumerate(keys):
        ht.insert(key, i)

    for i, key in enumerate(keys):
        assert ht.search(key) == i


def test_collision_delete_middle(ht):
    keys = ["аб", "ав", "аг"]

    for i, key in enumerate(keys):
        ht.insert(key, i)

    ht.delete("ав")

    assert ht.search("аб") == 0
    assert ht.search("аг") == 2

    with pytest.raises(Exception):
        ht.search("ав")


def test_duplicate_key(ht):
    ht.insert("аб", 1)
    with pytest.raises(Exception):
        ht.insert("аб", 2)

def test_search_not_found(ht):
    with pytest.raises(Exception):
        ht.search("аб")

def test_delete_head_of_chain(ht):
    ht.insert("аб", 1)
    ht.insert("ав", 2)

    ht.delete("аб")

    assert ht.search("ав") == 2


def test_delete_tail(ht):
    ht.insert("аб", 1)
    ht.insert("ав", 2)

    ht.delete("ав")

    assert ht.search("аб") == 1


def test_load_factor(ht):
    ht.insert("аб", 1)
    ht.insert("ав", 2)

    assert ht.get_load_factor() == 2 / ht.size

def test_clear(ht):
    ht.insert("аб", 1)
    ht.insert("ав", 2)

    ht.clear()

    with pytest.raises(Exception):
        ht.search("аб")

    assert ht.get_load_factor() == 0

def test_short_key(ht):
    with pytest.raises(Exception):
        ht.insert("а", 1)


def test_invalid_characters(ht):
    with pytest.raises(Exception):
        ht.insert("a1", 1)
        ht.insert("a1", 1)

def test_table_overflow():
    ht = HashTable(size=3)

    ht.insert("аб", 1)
    ht.insert("ав", 2)
    ht.insert("аг", 3)

    with pytest.raises(Exception):
        ht.insert("ад", 4)

def test_collision(ht):
    ht.insert("аб", 1)
    ht.insert("абв", 1)
    ht.insert("ав", 1)
