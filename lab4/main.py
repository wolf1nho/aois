from src.HashTable import HashTable

class Menu:
    def __init__(self):
        self.hash_table = HashTable()
        self.preload_data()

    def preload_data(self):
        data = [
            ("Абаев", "Тимур"),      # V[Аб] = 0*33 + 1 = 1. h = 1 % 20 = 1
            ("Астапов", "Андрей"),    # V[Бо] = 1*33 + 15 = 48. h = 48 % 20 = 8
            ("Видерт", "Руслан"),    # V[Ви] = 2*33 + 9 = 75. h = 75 % 20 = 15
            
            # Добавляем фамилии из Таблицы 1 документа:
            ("Гракова", "Наталья"),     # V[Вя] = 2*33 + 32 = 98. h = 98 % 20 = 18
            ("Кожевников", "Константин"),  # V[Ко] = 11*33 + 15 = 378. h = 378 % 20 = 18 (КОЛЛИЗИЯ с Вяткиным)
            ("Ковалев", "Сергей"),    # V[Ко] = 11*33 + 15 = 378. h = 18 (КОЛЛИЗИЯ, пойдет в ячейку 19 или 0)
            
            # Другие примеры для разнообразия хеш-адресов:
            ("Крикунов", "Евгений"), # V[Тр] = 19*33 + 17 = 644. h = 644 % 20 = 4
            ("Кот", "Иван"),      # V[Ив] = 8*33 + 2 = 266. h = 266 % 20 = 6
            ("Давыденко", "Ирина"),      # V[Пе] = 16*33 + 5 = 533. h = 533 % 20 = 13
            ("Горбань", "Петр"),    # V[Си] = 18*33 + 9 = 603. h = 603 % 20 = 3
            ("Данилов", "Павел"),  # V[Як] = 32*33 + 11 = 1067. h = 1067 % 20 = 7
            ("Козлов", "Максим"),
            ("Азимов", "Александр")
        ]
        print(">>> Предзагрузка данных...\n")

        for key, value in data:
            try:
                print(f"Добавляем: {key} → {value}")
                self.hash_table.insert(key, value)
            except Exception as e:
                print(f"Ошибка при добавлении {key}: {e}")

    def run(self):
        while True:
            self.print_menu()
            choice = input("Выберите действие: ")

            match choice:
                case "1":
                    self.insert()
                case "2":
                    self.search()
                case "3":
                    self.update()
                case "4":
                    self.delete()
                case "5":
                    self.display()
                case "6":
                    self.clear_table()
                case "7":
                    self.load_factor()
                case "0":
                    print("Выход...")
                    break
                case _:
                    print("Неверный ввод!")

    def print_menu(self):
        print("\n=== МЕНЮ ===")
        print("1. Добавить запись")
        print("2. Найти запись")
        print("3. Обновить запись")
        print("4. Удалить запись")
        print("5. Показать таблицу")
        print("6. Очистить таблицу")
        print("7. Коэффициент заполнения")
        print("0. Выход")

    def insert(self):
        key = input("Введите ключ (фамилия): ")
        value = input("Введите значение: ")
        try:
            self.hash_table.insert(key, value)
            print("Запись добавлена.")
        except Exception as e:
            print(f"Ошибка при добавлении записи: {e}")

    def display(self):
        headers = ["Idx", "ID", "V", "h", "C", "U", "P0", "Value"]
        print(" | ".join(f"{h:<10}" for h in headers))
        print("-" * 102)

        for i, node in enumerate(self.hash_table.table):
            if node.U:
                V = self.hash_table._get_value(node.key)
                h = self.hash_table._hash(node.key)
                key = node.key
                value = node.value
            else:
                V = ""
                h = ""
                key = ""
                value = ""
            P0 = node.P0 if node.P0 is not None else ""
                
            print(
                f"{i:<10} | "
                f"{key:<10} | "
                f"{V:<10} | "
                f"{h:<10} | "
                f"{node.C:<10} | "
                f"{node.U:<10} | "
                f"{P0:<10} | "
                f"{value:<10}"
            )

    def search(self):
        key = input("Введите ключ для поиска: ")
        try:
            value = self.hash_table.search(key)
            print(f"Значение для '{key}': {value}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def update(self):
        key = input("Введите ключ для обновления: ")
        try:
            self.hash_table.search(key)
        except Exception as e:
            print(f"Ошибка: {e}")
            return

        new_value = input("Введите новое значение: ")
        try:
            self.hash_table.update(key, new_value)
            print("Запись обновлена.")
        except Exception as e:
            print(f"Ошибка при обновлении записи: {e}")

    def delete(self):
        key = input("Введите ключ для удаления: ")
        try:
            self.hash_table.delete(key)
            print("Запись удалена.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def load_factor(self):
        try:
            print("Коэффициент заполнения:", self.hash_table.get_load_factor())
        except Exception as e:
            print("Ошибка:", e)

    def clear_table(self):
        self.hash_table.clear()
            
if __name__ == "__main__":
    menu = Menu()
    menu.run()