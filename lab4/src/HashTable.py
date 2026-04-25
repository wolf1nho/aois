from typing import Any

from src.constants import SIZE
from src.HashTableNode import HashTableNode

class HashTable:
    def __init__(self, size = SIZE) -> None:
        self.size: int = size
        self.table: list[HashTableNode] = [HashTableNode() for _ in range(size)]
        
    def _ru_letter_to_int(self, letter) -> int:
        val = ord(letter) - 1072
        if val < 6: #абвгде
            return val
        elif val == 33: # ё
            return 6
        else: # все остальное
            return val + 1

    def _get_value(self, key) -> int:
        return self._ru_letter_to_int(key[0].lower()) * 33 + self._ru_letter_to_int(key[1].lower())

    def _hash(self, key) -> int:
        return self._get_value(key) % self.size
    
    def _probe(self, index, i) -> int:
        return (index + i) % self.size

    def _write_node(self, index, key, value, *, c=False,  p0=None) -> None:
        node = self.table[index]
        node.key = key
        node.value = value
        node.U = True
        node.P0 = p0
        node.C = c

    def _clear_node(self, index) -> None:
        node = self.table[index]
        node.key = None
        node.value = None
        node.C = False
        node.U = False
        node.P0 = None

    def _find_free_slot(self, start_index) -> int | None:
        i = 1
        while i < self.size:
            idx = self._probe(start_index, i)
            if not self.table[idx].U:
                return idx
            i += 1
        raise Exception("Ошибка! Хеш-таблица переполнена, нет резервных ячеек.")

    def _find_previous_in_chain(self, index) -> int | None:
        node = self.table[index]
        if not node.U:
            return None

        base_index = self._hash(node.key)
        if base_index == index:
            return None

        curr_idx = base_index
        while curr_idx is not None:
            curr_node = self.table[curr_idx]
            if curr_node.P0 == index:
                return curr_idx
            if curr_node.P0 is None:
                break
            curr_idx = curr_node.P0

        return None
    
    def insert(self, key, value) -> None:
        h = self._hash(key)
        base_node = self.table[h]

        if not base_node.U:
            self._write_node(h, key, value, c=True)
            return

        # В базовой ячейке может лежать элемент, который относится к другой цепочке.
        # Тогда его нужно перенести, иначе поиск от адреса h не найдет новый ключ.
        if not base_node.C:
            free_idx = self._find_free_slot(h)
            if free_idx is None:
                raise Exception("Хеш-таблица переполнена, нет резервных ячеек.")

            prev_idx = self._find_previous_in_chain(h)
            self._write_node(
                free_idx,
                base_node.key,
                base_node.value,
                c=base_node.C,
                p0=base_node.P0
            )
            if prev_idx is not None:
                self.table[prev_idx].P0 = free_idx

            self._clear_node(h)
            self._write_node(h, key, value, c=True)
            return

        if base_node.key == key:
            raise Exception(f"Ключевое слово '{key}' уже существует в таблице.")

        curr_idx = h
        while True:
            node = self.table[curr_idx]

            if node.key == key:
                raise Exception(f"Ключевое слово '{key}' уже существует в таблице.")

            if node.P0 is None:
                break

            curr_idx = node.P0

        free_idx = self._find_free_slot(h)
        if free_idx is None:
            raise Exception("Ошибка! Хеш-таблица переполнена, нет резервных ячеек.")

        self._write_node(free_idx, key, value)
        tail_node = self.table[curr_idx]
        tail_node.P0 = free_idx
        return

    def search(self, key) -> Any:
        h = self._hash(key)
        curr_idx = h

        while True:
            if self.table[curr_idx].key == key:
                return self.table[curr_idx].value  # Ключ найден
            
            if self.table[curr_idx].P0 is None: # Если дошли до конца цепочки и не нашли
                raise Exception(f"Ключ '{key}' не найден.")  # Достигнут конец цепочки, ключ не найден
            
            curr_idx = self.table[curr_idx].P0

    def update(self, key, value) -> None:
        h = self._hash(key)
        curr_idx = h

        while True:
            if self.table[curr_idx].key == key:
                self.table[curr_idx].value = value  # Ключ найден, обновляем значение
                return
            
            if self.table[curr_idx].P0 is None:
                raise Exception("Ключ не найден")  # Достигнут конец цепочки, ключ не найден
            
            curr_idx = self.table[curr_idx].P0

    def delete(self, key) -> None:
        h = self._hash(key)
        curr_idx = h
        prev_idx = None

        # 1. Ищем элемент в цепочке
        while curr_idx is not None:
            node = self.table[curr_idx]
            
            # Если нашли ключ и он не был удален ранее
            if node.key == key and node.U:
                # Сценарий А: Элемент терминальный (конец цепочки)
                if node.P0 is None:
                    node.U = False
                    node.key = None
                    node.value = None
                    
                    # Если был предыдущий элемент в цепочке, делаем его терминальным
                    if prev_idx is not None:
                        self.table[prev_idx].P0 = None
                        
                # Сценарий Б: Элемент в середине цепочки
                else:
                    next_node = self.table[node.P0]
                    node.key = next_node.key
                    node.value = next_node.value
                    node.P0 = next_node.P0
                    next_node.value = None
                    next_node.key = None
                    next_node.U = False
                    next_node.P0 = None
                
                return
            
            if node.P0 is None: # Если дошли до конца цепочки и не нашли
                break

            prev_idx = curr_idx
            curr_idx = node.P0

        raise Exception(f"Ошибка: Ключ '{key}' не найден.")

    def clear(self) -> None:
        for i in range(0, self.size):
            self._clear_node(i)
            
    def get_load_factor(self) -> float:
        # Считаем только те ячейки, где флаг U (занято) равен True
        occupied_nodes = sum(1 for node in self.table if node.U)
        return occupied_nodes / self.size