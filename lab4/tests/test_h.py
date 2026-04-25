import pytest
from HashTable import HashTable


@pytest.fixture
def ht():
    return HashTable(size=10)


# ----------------------
# БАЗОВЫЕ ОПЕРАЦИИ
# ----------------------

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


# ----------------------
# КОЛЛИЗИИ
# ----------------------

def test_collision_chain(ht):
    # Подбираем ключи с одинаковым хешем
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


# ----------------------
# ДУБЛИКАТЫ
# ----------------------

def test_duplicate_key(ht):
    ht.insert("аб", 1)
    with pytest.raises(Exception):
        ht.insert("аб", 2)


# ----------------------
# ПОИСК НЕСУЩЕСТВУЮЩЕГО
# ----------------------

def test_search_not_found(ht):
    with pytest.raises(Exception):
        ht.search("аб")


# ----------------------
# DELETE: РАЗНЫЕ СЛУЧАИ
# ----------------------

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


# ----------------------
# LOAD FACTOR
# ----------------------

def test_load_factor(ht):
    ht.insert("аб", 1)
    ht.insert("ав", 2)

    assert ht.get_load_factor() == 2 / ht.size


# ----------------------
# CLEAR
# ----------------------

def test_clear(ht):
    ht.insert("аб", 1)
    ht.insert("ав", 2)

    ht.clear()

    with pytest.raises(Exception):
        ht.search("аб")

    assert ht.get_load_factor() == 0


# ----------------------
# ГРАНИЧНЫЕ СЛУЧАИ
# ----------------------

def test_short_key(ht):
    with pytest.raises(Exception):
        ht.insert("а", 1)


def test_invalid_characters(ht):
    with pytest.raises(Exception):
        ht.insert("a1", 1)
        ht.insert("a1", 1)



# ----------------------
# ПЕРЕПОЛНЕНИЕ
# ----------------------

def test_table_overflow():
    ht = HashTable(size=3)

    ht.insert("аб", 1)
    ht.insert("ав", 2)
    ht.insert("аг", 3)

    with pytest.raises(Exception):
        ht.insert("ад", 4)