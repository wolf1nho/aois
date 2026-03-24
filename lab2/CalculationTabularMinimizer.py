class CalculationTabularMinimizer:
    def __init__(self):
        self.table = []
        self.variables = []
        self.minimized_sdnf = ""
        self.minimized_sknf = ""

    def minimize_sdnf(self, table, variables):
        self.table = table
        self.variables = variables
        
        if not self.table:
            return "0"

        # Шаг 1: Извлекаем термы, где функция равна 1
        minimized_terms = [row[:-1] for row in self.table if row[-1] == 1]
        
        if not minimized_terms:
            self.minimized_sdnf = "0"
            return "0"
        
        initial_terms = [tuple(t) for t in minimized_terms] # Сохраняем для таблицы покрытий
        
        # Шаг 2: Поиск простых импликант (Склеивание)
        current_terms = set(tuple(t) for t in minimized_terms)
        prime_implicants = set()

        while True:
            next_terms = set()
            used = set()
            term_list = list(current_terms)
            
            for i in range(len(term_list)):
                for j in range(i + 1, len(term_list)):
                    diff_count = 0
                    diff_index = -1
                    
                    for k in range(len(term_list[i])):
                        if term_list[i][k] != term_list[j][k]:
                            diff_count += 1
                            diff_index = k
                    
                    # Если отличаются ровно в одном бите — склеиваем
                    if diff_count == 1:
                        new_term = list(term_list[i])
                        new_term[diff_index] = 2 # 2 заменяет прочерк (-)
                        next_terms.add(tuple(new_term))
                        used.add(term_list[i])
                        used.add(term_list[j])
            
            # Добавляем те, что не склеились, в простые импликанты
            for t in current_terms:
                if t not in used:
                    prime_implicants.add(t)
            
            if not next_terms:
                break
            current_terms = next_terms

        # Шаг 3: Построение таблицы покрытий и поиск минимального набора
        prime_list = list(prime_implicants)
        # Матрица: строки — простые импликанты, столбцы — исходные термы (минтермы)
        chart = [[False] * len(initial_terms) for _ in range(len(prime_list))]
        
        for i, prime in enumerate(prime_list):
            for j, start in enumerate(initial_terms):
                match = True
                for k in range(len(variables)):
                    if prime[k] != 2 and prime[k] != start[k]:
                        match = False
                        break
                chart[i][j] = match

        # Шаг 4: Выбор импликант (упрощенный поиск ядер)
        selected_indices = set()
        covered_columns = [False] * len(initial_terms)

        # Находим обязательные импликанты (ядра)
        for j in range(len(initial_terms)):
            count = 0
            last_i = -1
            for i in range(len(prime_list)):
                if chart[i][j]:
                    count += 1
                    last_i = i
            if count == 1:
                selected_indices.add(last_i)

        # Помечаем, какие столбцы уже покрыты ядрами
        for idx in selected_indices:
            for j in range(len(initial_terms)):
                if chart[idx][j]:
                    covered_columns[j] = True

        # Если остались непокрытые столбцы, добираем импликанты (жадный алгоритм)
        while not all(covered_columns):
            best_i = -1
            max_new_cover = 0
            for i in range(len(prime_list)):
                if i not in selected_indices:
                    new_cover = sum(1 for j in range(len(initial_terms)) if chart[i][j] and not covered_columns[j])
                    if new_cover > max_new_cover:
                        max_new_cover = new_cover
                        best_i = i
            if best_i != -1:
                selected_indices.add(best_i)
                for j in range(len(initial_terms)):
                    if chart[best_i][j]:
                        covered_columns[j] = True
            else:
                break

        # Шаг 5: Сборка финальной строки
        result_parts = []
        for idx in selected_indices:
            term = prime_list[idx]
            part = ""
            for i in range(len(variables)):
                if term[i] == 1:
                    part += variables[i]
                elif term[i] == 0:
                    part += f"!{variables[i]}"
            result_parts.append(part)
        
        self.minimized_sdnf = " | ".join(result_parts) if result_parts else "0"



    def minimize_sknf(self, table, variables):
        self.table = table
        self.variables = variables
        
        if not self.table:
            return "1" # Для пустой таблицы по умолчанию истина

        # Шаг 1: Извлекаем макстермы (где функция равна 0)
        # В СКНФ мы работаем с нулями
        minimized_terms = [row[:-1] for row in self.table if row[-1] == 0]
        
        if not minimized_terms:
            self.minimized_sknf = "1"
            return "1"
        
        initial_terms = [tuple(t) for t in minimized_terms]
        
        # Шаг 2: Поиск простых имплицент (Склеивание)
        current_terms = set(tuple(t) for t in minimized_terms)
        prime_implicants = set()

        while True:
            next_terms = set()
            used = set()
            term_list = list(current_terms)
            
            for i in range(len(term_list)):
                for j in range(i + 1, len(term_list)):
                    diff_count = 0
                    diff_index = -1
                    
                    for k in range(len(term_list[i])):
                        if term_list[i][k] != term_list[j][k]:
                            diff_count += 1
                            diff_index = k
                    
                    if diff_count == 1:
                        new_term = list(term_list[i])
                        new_term[diff_index] = 2 # Прочерк
                        next_terms.add(tuple(new_term))
                        used.add(term_list[i])
                        used.add(term_list[j])
            
            for t in current_terms:
                if t not in used:
                    prime_implicants.add(t)
            
            if not next_terms:
                break
            current_terms = next_terms

        # Шаг 3: Таблица покрытий
        prime_list = list(prime_implicants)
        chart = [[False] * len(initial_terms) for _ in range(len(prime_list))]
        
        for i, prime in enumerate(prime_list):
            for j, start in enumerate(initial_terms):
                match = True
                for k in range(len(variables)):
                    if prime[k] != 2 and prime[k] != start[k]:
                        match = False
                        break
                chart[i][j] = match

        # Шаг 4: Выбор минимального покрытия (Ядра + Жадный выбор)
        selected_indices = set()
        covered_columns = [False] * len(initial_terms)

        for j in range(len(initial_terms)):
            count = sum(1 for i in range(len(prime_list)) if chart[i][j])
            if count == 1:
                for i in range(len(prime_list)):
                    if chart[i][j]:
                        selected_indices.add(i)
                        break

        for idx in selected_indices:
            for j in range(len(initial_terms)):
                if chart[idx][j]:
                    covered_columns[j] = True

        while not all(covered_columns):
            best_i = -1
            max_new_cover = 0
            for i in range(len(prime_list)):
                if i not in selected_indices:
                    new_cover = sum(1 for j in range(len(initial_terms)) if chart[i][j] and not covered_columns[j])
                    if new_cover > max_new_cover:
                        max_new_cover = new_cover
                        best_i = i
            if best_i != -1:
                selected_indices.add(best_i)
                for j in range(len(initial_terms)):
                    if chart[best_i][j]:
                        covered_columns[j] = True
            else:
                break

        # Шаг 5: Сборка финальной строки СКНФ
        # Напоминаю: в СКНФ 0 -> x, 1 -> ¬x, соединяем через ∨
        result_parts = []
        for idx in selected_indices:
            term = prime_list[idx]
            clause = []
            for i in range(len(variables)):
                if term[i] == 0:
                    clause.append(variables[i])
                elif term[i] == 1:
                    clause.append(f"!{variables[i]}")
            
            # Если в терме больше одной переменной, берем в скобки
            if len(clause) > 1:
                result_parts.append(f"({' | '.join(clause)})")
            else:
                result_parts.append(clause[0])

        self.minimized_sknf = " & ".join(result_parts) if result_parts else "0"
        return self.minimized_sknf

    def get_minimized_sdnf(self):
        return self.minimized_sdnf

    def get_minimized_sknf(self):
        return self.minimized_sknf

        

        
