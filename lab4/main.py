from src.HashTable import HashTable

class Menu:
    def __init__(self):
        self.hash_table = HashTable()
        self.preload_data()

    def preload_data(self):
        data = [
            ("Абаев", "Тимур"),      
            ("Астапов", "Андрей"),
            ("Видерт", "Руслан"),
            
            ("Гракова", "Наталья"),
            ("Кожевников", "Константин"),
            ("Ковалев", "Сергей"),

            ("Крикунов", "Евгений"),
            ("Кот", "Иван"),
            ("Давыденко", "Ирина"),
            ("Горбань", "Петр"),
            ("Данилов", "Павел"),
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